import re
from pathlib import Path

import git

from app.config import settings
from app.utils.log_utils import Log

logger = Log().get_logger()


class GitUtil:

    def __init__(self, git_url: str = None):
        """
        :param git_url: 远程地址
        """
        self.git_url = git_url
        self.repo_dir = settings.local_repository.joinpath(self.get_repo_name())

    def get_repo_name(self):
        # 处理SSH格式 (git@github.com:username/repo.git)
        ssh_pattern = r'git@.*?:(.*?)(\.git)?$'
        ssh_match = re.search(ssh_pattern, self.git_url)
        if ssh_match:
            path = ssh_match.group(1)
            return Path(path).name

        # 处理HTTPS格式 (https://github.com/username/repo.git)
        https_pattern = r'https?://.*?/(.*?)(\.git)?$'
        https_match = re.search(https_pattern, self.git_url)
        if https_match:
            path = https_match.group(1)
            return Path(path).name

    def clone_or_pull(self):
        if self.repo_dir.is_dir():
            logger.info(f"目标目录已存在，从远程拉取最新数据: {self.repo_dir}")
            self.pull()
        else:
            logger.info(f"目标目录不存在，从远程 clone 仓库: {self.repo_dir}")
            self.clone()

    def clone(self):
        """克隆指定的 Git 仓库到给定目录"""
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
        return [branch.name for branch in repo.branches]

    def get_local_repo_hash(self):
        """获取本地仓库最后一个 commit 的 hash"""
        repo = git.Repo(self.repo_dir)
        return repo.head.commit.hexsha


if __name__ == "__main__":
    # 如果配置了 ssh 密钥认证
    remote_url = "git@github.com:MyNextWeekend/fastapi_project.git"
    # 也可以执行提供账号密码(不安全不推荐)
    # remote_url="https://username:password@github.com/your-username/your-repo.git"
    # 使用访问令牌通常比使用密码更安全
    token = "ghp_dajiblVNtaXWhmTT0gVjxxxxxxxxxx"
    # remote_url = f"https://{token}@github.com/MyNextWeekend/fastapi_project.git"

    git_obj = GitUtil(remote_url)
    git_obj.clone_or_pull()
    print(git_obj.get_local_repo_hash())
    # print(git_obj.repo_dir)
    # git_obj.clone()
    # print(git_obj.get_repo_name())
    # print(git_obj.list_branches())
