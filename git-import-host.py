#!/usr/bin/env python3

import argparse
import json
from datetime import date, timedelta

import censys.search
import git
import jsonpatch


class CensysEntry:
    def __init__(self, host, at_time, censys_ctx) -> None:
        self.host = host
        self.at_time = at_time
        self.to_time = at_time + timedelta(days=1)
        self.censys_ctx = censys_ctx
        self.data = self.censys_ctx.view(self.host, at_time=self.at_time)
        self.diff = self.censys_ctx.view_host_diff(
            self.host, at_time=self.at_time, at_time_b=self.to_time
        )
        self.patches = self.diff["patch"]

    def apply_patch(self):
        return jsonpatch.apply_patch(self.data, self.patches)


class CensysManager:
    def __init__(self, host, start_date, end_date, repo="./"):
        self.host = host
        self.start_date = start_date
        self.end_date = end_date
        self.repo = repo
        self.entries = self._generate_entries()

    def _generate_entries(self):
        h = censys.search.CensysHosts()
        entries = []
        current_date = self.start_date
        while current_date <= self.end_date:
            entries.append(CensysEntry(self.host, current_date, h))
            current_date += timedelta(days=1)
        return entries

    def _is_operation_filtered(self, patch):
        # for a clean commit history, we will take these fields into account,
        # but not actually commit each one.
        filtered = {
            "replace": [
                "source_ip",
                "perspective_id",
                "observed_at",
                "last_updated_at",
            ]
        }
        if patch["op"] in filtered:
            for path in filtered[patch["op"]]:
                if path in patch["path"]:
                    return True

        return False

    def save_to_repo(self, use_branch=""):
        repository = None
        repository = git.Repo(self.repo)

        if use_branch != "":
            branch = repository.create_head(use_branch)
            repository.head.reference = branch

        first_data = self.entries[0].data
        filename = f"{self.repo}/{self.host}"

        with open(filename, "w+", newline="\n") as f:
            f.write(json.dumps(first_data, indent=2))
            repository.index.add([f"{self.host}"])
            repository.index.commit(f"Update {self.host}")

        is_dangling = False
        for entry in self.entries:
            for patch in entry.patches:
                first_data = jsonpatch.apply_patch(first_data, [patch])
                with open(filename, "w", newline="\n") as f:
                    f.write(json.dumps(first_data, indent=2))
                    f.flush()

                if self._is_operation_filtered(patch):
                    is_dangling = True
                    continue

                is_dangling = False
                repository.git.commit(
                    "--date",
                    entry.at_time,
                    "-a",
                    "-m",
                    f'{patch["op"]} {patch["path"]}',
                )
        if is_dangling:
            # this is a dumb way to handle this.
            repository.git.commit("-a", "-m", "final")


def _is_censys_repo(repo):
    try:
        with open(f"{repo}/.censys"):
            return True
    except FileNotFoundError:
        return False


def _needs_init(repo):
    try:
        _ = git.Repo(repo).git_dir
        return False
    except git.exc.InvalidGitRepositoryError:
        return True


def main(args):
    if args.host == "init" and _needs_init(args.repo):
        print("Initializing new Censys host import repository.")

        with open(f"{args.repo}/.censys", "w+") as f:
            f.write("This is a Censys host import repository.")

        repo = git.Repo.init(args.repo)
        repo.index.add([".censys"])
        repo.git.commit("-a", "-m", "Initial commit")
        print("Initialized new Censys host import repository.")
        exit(0)

    if not _is_censys_repo(args.repo):
        print("Error: not a censys host import repository (use 'init' to create one).")
        exit(1)

    if args.from_date is None or args.to_date is None:
        print("Error: --from-date and --to-date are required")
        exit(1)

    manager = CensysManager(args.host, args.from_date, args.to_date, repo=args.repo)
    manager.save_to_repo(use_branch=args.branch)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process Censys data and save to git repo."
    )
    parser.add_argument("host", help="Host IP to process")
    parser.add_argument(
        "-f",
        "--from-date",
        type=lambda s: date.fromisoformat(s),
        help="Start date in the format YYYY-MM-DD",
    )
    parser.add_argument(
        "-t",
        "--to-date",
        type=lambda s: date.fromisoformat(s),
        help="End date in the format YYYY-MM-DD",
    )
    parser.add_argument("-r", "--repo", default=".", help="Path to git repo")
    parser.add_argument(
        "-b", "--branch", default="", help="Create a new branch and import the host."
    )
    args = parser.parse_args()

    main(args)
