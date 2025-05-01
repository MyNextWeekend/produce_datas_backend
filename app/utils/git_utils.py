import os

import git

from app.utils.log_utils import Log

logger = Log().get_logger()


class GitUtil:

    def __init__(self, repo_dir: str, git_url: str = None):
        """
        :param git_url: 远程地址
        :param repo_dir: 仓库本地目录
        """
        self.repo_dir = repo_dir
        self.git_url = git_url

    def clone(self):
        """克隆指定的 Git 仓库到给定目录"""
        if os.path.isdir(self.repo_dir):
            logger.error(f"目标目录已存在: {self.repo_dir}")
            raise RuntimeError(f"目标目录已存在: {self.repo_dir}")
        if self.git_url is None:
            logger.error("远程 url 为空")
            raise RuntimeError("远程 url 为空")

        git.Repo.clone_from(self.git_url, self.repo_dir)
        logger.info(f"git clone success: from {self.git_url} to {self.repo_dir}")

    def pull(self, remote_name: str = "origin", branch_name: str = "main"):
        """从远程仓库拉取更改"""
        repo = git.Repo(self.repo_dir)
        repo.remotes[remote_name].pull(branch_name)
        logger.info(f"git pull success: {self.repo_dir} - {branch_name}")

    def status(self):
        """检查指定目录中的 Git 仓库状态"""
        repo = git.Repo(self.repo_dir)
        return repo.git.status()

    def checkout(self, branch_name):
        """切换到指定的分支"""
        repo = git.Repo(self.repo_dir)
        repo.git.checkout(branch_name)
        logger.info(f"git checkout success: {self.repo_dir} - {branch_name}")

    def list_branches(self):
        """列出所有分支"""
        repo = git.Repo(self.repo_dir)
        return [branch.name for branch in repo.branches()]


if __name__ == "__main__":
    local_dir = "/Users/weekend/workSpaces/pycharmProjects/fastapi_project/aaa"
    # 如果配置了 ssh 密钥认证
    # remote_url = "git@github.com:MyNextWeekend/fastapi_project.git"
    # 也可以执行提供账号密码(不安全不推荐)
    # remote_url="https://username:password@github.com/your-username/your-repo.git"
    # 使用访问令牌通常比使用密码更安全
    token = "ghp_dajiblVNtaXWhmTT0gVjxxxxxxxxxx"
    remote_url = f"https://{token}@github.com/MyNextWeekend/fastapi_project.git"

    git_obj = GitUtil(local_dir, remote_url)
    git_obj.clone()
