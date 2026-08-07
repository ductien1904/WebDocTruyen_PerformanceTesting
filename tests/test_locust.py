from locust import HttpUser, task, between, tag
import random


class UTTPortalUser(HttpUser):
    host = "http://localhost"
    wait_time = between(1, 5)

    def on_start(self):
        self.client.post(
            "/web_doc_truyen/frontend/view/log/login.html",
            data={
                "username": "dangnhap",
                "password": "makhau"
            }
        )

    @task(3)
    def trangChu(self):
        self.client.get(
            "/web_doc_truyen/frontend/public/index.html",
            name="Trang chu"
        )

    @tag('chuong_management')
    @task(2)
    def chuongManagement(self):
        urls = [
            ("/web_doc_truyen/frontend/view/chuong/add.html",    "Chuong - add"),
            ("/web_doc_truyen/frontend/view/chuong/delete.html", "Chuong - delete"),
            ("/web_doc_truyen/frontend/view/chuong/edit.html",   "Chuong - edit"),
        ]
        for url, name in urls:
            self.client.get(url, name=name)