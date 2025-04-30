# fastapiProject 记录学习

---

> 关于我
> 博客：[无](http://)



~~~shell
#  Run a FastAPI app in development mode. 🧪 
fastapi dev

# Run a FastAPI app in production mode. 🚀  
fastapi run

# 手动运行服务
# --reload 选项消耗更多资源,不应该在生产环境中使用它
uv run uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
~~~