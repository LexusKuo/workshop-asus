---
name: "Lab 1: Product search"
about: Implement product search, sorting, and pagination API
title: "Lab 1 | 使用 Copilot Coding Agent 完成 Issue to PR - Product Search API"
---

## 目標

根據 `docs/lab-1-agentic-workflow.md` 的要求，實現 `GET /products` API 的完整搜尋、排序和分頁功能。

## Context

Starter 應用已經有基本的 API 結構。需要通過補足 query parameters 和驗證邏輯來完成產品搜尋功能。

## API 行為規格

`GET /products` 接受以下 optional query parameters：

| Parameter | 規則 | 預設值 |
|---|---|---|
| `q` | 對產品名稱或分類執行不區分大小寫的 partial match | 無 |
| `sort` | 僅允許 `name` 或 `price`；無效值回傳 HTTP 422 | 無 |
| `order` | 僅允許 `asc` 或 `desc`；無效值回傳 HTTP 422 | `asc` |
| `page` | 大於或等於 1 的整數；無效值回傳 HTTP 422 | 1 |
| `page_size` | 1 到 20 的整數；無效值回傳 HTTP 422 | 20 |

### Response 規格

- 必須維持既有的 `items`、`total`、`page`、`page_size` 結構
- `total` 代表分頁前的符合筆數（搜尋和排序應用後，但在分頁 slicing 前計算）
- 搜尋、排序與分頁必須能組合使用
- 既有的 `GET /products/{product_id}` 行為不得改變

## Acceptance Criteria

- [ ] **搜尋功能** - `q` parameter 對產品名稱和分類執行不區分大小寫的 partial match
- [ ] **排序字段驗證** - `sort` 僅接受 `name` 或 `price`；其他值回傳 HTTP 422
- [ ] **排序順序驗證** - `order` 僅接受 `asc` 或 `desc`；預設 `asc`；其他值回傳 HTTP 422
- [ ] **分頁驗證** - `page` 必須 ≥ 1；預設 1；無效值回傳 HTTP 422
- [ ] **每頁筆數驗證** - `page_size` 必須在 1 到 20 之間；預設 20；無效值回傳 HTTP 422
- [ ] **Total 計算** - `total` 在 pagination slicing 前計算（搜尋和排序應用後）
- [ ] **組合功能** - 搜尋、排序和分頁能正確組合使用
- [ ] **回應結構** - Response 保持原有的 `items`、`total`、`page`、`page_size` 結構
- [ ] **向後相容** - 既有的 `GET /products/{product_id}` 行為保持不變
- [ ] **基礎驗證通過** - `python scripts/validate.py` 通過
- [ ] **Lab 1 測試通過** - `pytest -q -m lab1` 通過

## 驗證命令

```bash
# 確認 Starter 狀態
python scripts/preflight.py
python scripts/validate.py

# 在 Swagger UI 開啟 /products 確認 API response

# 實現後驗證
pytest -q -m lab1
```

## Coding Agent 檢查點

指派給 Copilot Coding Agent 時，請確認 Agent 的 plan 包含：

1. **Input Validation** - 使用 FastAPI/Pydantic constraints 進行驗證，而非手動字串判斷
2. **執行順序** - filter → sort → pagination 的正確順序
3. **相容性** - 所有參數組合都應正確工作
4. **測試覆蓋** - 既有測試通過，新增 Lab 1 acceptance tests 通過

## PR Review 檢查清單

- [ ] Diff 僅包含需求必要的修改
- [ ] 使用 FastAPI/Pydantic constraints，而非手動字串判斷
- [ ] `total` 在 pagination slicing 前計算
- [ ] 既有 tests 通過
- [ ] `pytest -q -m lab1` 通過
- [ ] CI 偵測到 product router 修改並執行 Lab 1 tests
- [ ] CI 為 green
- [ ] PR summary 說明 assumptions 與執行過的 commands

## 參考文件

- `docs/lab-1-agentic-workflow.md` - Lab 1 完整要求與指南
