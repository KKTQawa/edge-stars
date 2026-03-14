1. edge浏览器存放收藏夹位置位于`C:\Users\用户名\AppData\Local\Microsoft\Edge\User Data\Default\Bookmarks`
2. Bookmarks文件本质为json文件，结构大概为
   
```json
{
  "checksum": "xxxx",
  "roots": {
    "bookmark_bar": {
      "children": [
        {
          "date_added": "xxxx",
          "id": "xxxx",
          "name": "xxxx",
          "type": "url",
          "url": "xxxx"
        }
        ...
      ],
      "date_added": "xxxx",
      "date_modified": "xxxx",
      "id": "xxxx",
      "name": "xxx",
      "type": "xxx"
    },//收藏夹栏
    "other": {...},//其他收藏夹
    "synced": {...},//移动收藏夹
    ...
  },
  "sync_metadata": ”xxxx",
  "version": x
}
```

3. `export_star.py`读取并转换为md/html文件