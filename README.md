# 六合彩 7×7 走線視覺化

在 7×7 號碼表（1–49）上，用**虛線**把每期 6 個中獎號碼按順序連起來。同一行上連續號碼（例如 1→2→3→4→5→6）會呈一直線；下一個若在下一行（例如 8）則會折向下行。

## 使用方式

```bash
cd /workspace
python3 -m http.server 8080
```

瀏覽器打開 [http://localhost:8080](http://localhost:8080)。

- **滑桿**：切換期次（第 1 行 = 第 1 期）
- **只顯示本期**：單期虛線 + 圓點
- **疊加全部期次**：所有期次半透明虛線
- **熱力次數**：各號碼出現次數
- **連線順序**：預設「由小到大」；可改為列表原始順序
- 左側可貼上新資料並 **載入貼上資料**

## 資料檔

| 檔案 | 說明 |
|------|------|
| `data/draws.txt` | 你提供的 2543 期（每行 6 個號碼） |
| `data/draws.json` | 由 `scripts/parse_draws.py` 產生，供網頁載入 |

重新產生 JSON：

```bash
python3 scripts/parse_draws.py data/draws.txt data/draws.json
```

（可選）`scripts/fetch_hkjc_draws.py` 嘗試從 HKJC GraphQL 拉官方歷史；若 API 不可用，請以 `draws.txt` 為準。
