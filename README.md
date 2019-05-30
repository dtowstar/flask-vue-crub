flask-vue-crub
===

use vue+flask+python to auto get ticket

關於環境前端需要node.js<br>
因為前後端是分開的關係所以需要同時開啟才能溝通

使用說明
---

### 一般使用者
1.開啟一個cmd，並進入目標資料夾<br>
```
cd flask-vue-crub
```

2.建立虛擬環境，並進入虛擬環境<br>
```
python -m venv venv
venv\Scripts\activate
```

3.下載相依套件<br>
```
pip install -r requirements.txt
```

4.執行app.py<br>
```
python app.py
```

4.開啟瀏覽器，進入http://localhost:5000<br>

### 開發者(需修改vue)
1.開啟第二個cmd，並進入專案目錄<br>
```
cd flask-vue-crub
```
2.進入client目錄<br>
```
cd client
```
3.下載相依套件<br>
```
npm install
```
4.執行前端<br>
```
npm run dev
```
5.開啟瀏覽器，進入http://localhost:8080<br>
