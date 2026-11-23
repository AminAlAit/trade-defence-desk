"""Create the labels, milestones and issues of backlog/issues.json on GitHub.

Needs the GitHub CLI, logged in:  gh auth login
Run from the repository root:     python scripts/create_issues.py OWNER/REPO

Safe to run twice: labels are updated, and milestones and issues that already exist
(same id at the start of the title) are skipped. An issue that should be closed and is
still open is closed on the next run.
"""
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
RETRY_WORDS = ("rate limit", "secondary rate")


def gh(*args, tries=4):
    for attempt in range(tries):
        result = subprocess.run(["gh", *args], capture_output=True, text=True, encoding="utf-8")
        if result.returncode == 0:
            return result.stdout
        error = result.stderr.lower()
        if attempt + 1 < tries and any(word in error for word in RETRY_WORDS):
            time.sleep(30 * (attempt + 1))
            continue
        sys.exit("gh %s failed:\n%s" % (" ".join(args[:3]), result.stderr))


def main():
    if len(sys.argv) != 2 or "/" not in sys.argv[1]:
        sys.exit(__doc__)
    repo = sys.argv[1]
    data = json.loads((ROOT / "backlog" / "issues.json").read_text(encoding="utf-8"))

    ref = json.loads(gh("repo", "view", repo, "--json", "defaultBranchRef"))["defaultBranchRef"] or {}
    branch = ref.get("name") or "main"
    blob = "https://github.com/%s/blob/%s" % (repo, branch)

    for label in data["labels"]:
        gh("label", "create", label["name"], "--repo", repo, "--color", label["color"],
           "--description", label["description"], "--force")
    print("labels:", len(data["labels"]))

    have = {m["title"] for m in json.loads(gh("api", "repos/%s/milestones?state=all&per_page=100" % repo))}
    for ms in data["milestones"]:
        if ms["title"] in have:
            continue
        args = ["api", "repos/%s/milestones" % repo, "-f", "title=" + ms["title"],
                "-f", "description=" + ms["description"]]
        if ms["due_on"]:
            args += ["-f", "due_on=" + ms["due_on"]]
        gh(*args)
    print("milestones:", len(data["milestones"]))

    existing = json.loads(gh("issue", "list", "--repo", repo, "--state", "all", "--limit", "500",
                             "--json", "number,title,state"))
    numbers = {i["title"].split(":")[0]: i["number"] for i in existing}
    state = {i["title"].split(":")[0]: i["state"].lower() for i in existing}
    created = 0
    for issue in data["issues"]:
        key = issue["id"]
        if key not in numbers:
            handle, name = tempfile.mkstemp(suffix=".md")
            try:
                with os.fdopen(handle, "w", encoding="utf-8", newline="\n") as fh:
                    fh.write(issue["body"].replace("{{BLOB}}", blob))
                args = ["issue", "create", "--repo", repo, "--title", issue["title"], "--body-file", name,
                        "--milestone", issue["milestone"]]
                for label in issue["labels"]:
                    args += ["--label", label]
                url = gh(*args).strip().splitlines()[-1]
            finally:
                os.unlink(name)
            numbers[key] = int(url.rstrip("/").rsplit("/", 1)[-1])
            state[key] = "open"
            created += 1
            print(key, "->", numbers[key])
            time.sleep(1.5)
        if issue["state"] == "closed" and state[key] != "closed":
            gh("issue", "close", str(numbers[key]), "--repo", repo, "--comment", issue.get("close_comment", "Done."))

    out = {"repo": repo, "numbers": {i["id"]: numbers[i["id"]] for i in data["issues"]}}
    (ROOT / "backlog" / "issue_numbers.json").write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8",
                                                         newline="\n")
    print("issues created:", created, "of", len(data["issues"]))


if __name__ == "__main__":
    main()
