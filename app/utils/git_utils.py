import os

import git


def git_clone(git_url, repo_dir):
    """克隆指定的 Git 仓库到给定目录。

    参数:
        git_url (str): Git 仓库的 URL。
        repo_dir (str): 克隆目标目录。

    异常:
        Exception: 如果克隆失败，将引发异常，并包含错误信息。
    """
    if os.path.exists(repo_dir):
        raise Exception(f"目标目录已存在: {repo_dir}")

    try:
        git.Repo.clone_from(git_url, repo_dir)
        print("Git clone success")
    except git.exc.GitError as e:
        raise Exception(
            f"Git clone error: {e} - URL: {git_url}, Target Directory: {repo_dir}"
        )


def git_pull(repo_dir, remote_name="origin", branch_name="main"):
    """从远程仓库拉取更改。

    参数:
        repo_dir (str): 仓库所在目录。
        remote_name (str): 远程名称（默认为 'origin'）。
        branch_name (str): 分支名称（默认为 'main'）。
    """
    try:
        repo = git.Repo(repo_dir)
        repo.remotes[remote_name].pull(branch_name)
        print("Changes pulled successfully.")
    except git.exc.GitError as e:
        print(f"Error pulling from remote: {e}")


def git_status(repo_dir):
    """检查指定目录中的 Git 仓库状态。

    参数:
        repo_dir (str): 仓库所在目录。

    返回:
        str: 仓库的状态信息。
    """
    try:
        repo = git.Repo(repo_dir)
        status = repo.git.status()
        return status
    except git.exc.GitError as e:
        raise Exception(f"Git status error: {e} - Repository Directory: {repo_dir}")


def git_checkout(repo_dir, branch_name):
    """切换到指定的分支。

    参数:
        repo_dir (str): 仓库所在目录。
        branch_name (str): 要切换的分支名称。

    异常:
        Exception: 如果切换失败，将引发异常，并包含错误信息。
    """
    try:
        repo = git.Repo(repo_dir)
        repo.git.checkout(branch_name)
        print(f"Checked out to branch: {branch_name}")
    except git.exc.GitError as e:
        raise Exception(
            f"Git checkout error: {e} - Repository Directory: {repo_dir}, Branch: {branch_name}"
        )


def git_list_branches(repo_dir):
    """列出所有分支。

    参数:
        repo_dir (str): 仓库所在目录。

    返回:
        list: 分支名称列表。
    """
    try:
        repo = git.Repo(repo_dir)
        branches = [branch.name for branch in repo.branches]
        return branches
    except git.exc.GitError as e:
        print(f"Error listing branches: {e}")
        return []


if __name__ == "__main__":
    git_status("/Users/weekend/workSpaces/pycharmProjects/fastApiProject")
