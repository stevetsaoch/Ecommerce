# Tsao Books 網路書店

![Website tour](readme_figures/Website_tour.gif)

## 簡介

此網站是後端練習網站，由 <b>Django</b> 框架開發的 <b>MTV</b> 架構網路書店。後端由 <b>Class-based views</b> 為主輔以 <b>Function-based views</b> 作為業務邏輯層(V)，搭配 <b>MySQL</b> 作為資料庫(M)；前端頁面(T)則以原生 <b>Django template</b> 為主，搭配 <b>Jquery(ajax)</b> 與 <b>CSS</b> 實作互動功能與排版。
<br>
<br>

## 網頁Demo

<https://stevetsaoch.pythonanywhere.com/>

<br>

## 資料庫架構

![Database Diagram](readme_figures/Databases_diagram.png)

<br>

## 網站架構

```mermaid
flowchart LR
    subgraph Store[Store]
        direction TB
        I[Index] -.-> C[Category]
        C -.-> S
        I --> S[Single]
    end
    subgraph Bag
        direction RL
        S --> B[Shopping Bag]
        S -.-> W[Wishlist] 
        W -.-> B
    end

    subgraph Checkout
        B --> DS[Delivery Option]
        DS --> CA[Check Address]
        CA --> P[Paypal]
    end
    subgraph Orders
        P --> O[Order]
        O --> OI[Order issue]
    end
    subgraph Reviews
        O --> S --> R[Review]
    end    
```

__*備註: 實線箭頭：預設流程; 虛線箭頭：替代流程*__
<br>

## 主要練習

- Django
  - Class-based views
    - 重寫方法以符合業務需求
    - 嘗試以 REST 風格撰寫對應功能
  - Function-based views
  - Models, Forms
  - Eamil function
  - Session (購物袋管理)
  - Custom Template tags
  - Custom commands (生產假資料)
  - Token for authentication

- MySQL
  - 資料庫正規化(Normalization)

- 串接 Paypal 金流支付 API

- Jquery(Ajax)
  - 首頁翻頁、更新商品數量與刪除商品
  - 即時顯示評論
  - 紀錄商品點擊數 (用於找出Bestsellers)

- CSS
  - 製作簡易動畫(指向選項時改變背景，選取後產生陰影等)
  - Responsive Web Design
<br>

## 網頁內容介紹

- 商品頁面
  - 商品預覽、評分預覽
  - 最受歡迎商品
  - 促銷活動
- 使用者相關功能
  - 註冊
  - 登入、登出、更改密碼
  - 更新使用者資料
  - 刪除使用者
- 願望清單
  - 新增、刪除
  - 加入購物袋
- 購物車
  - 新增、刪除
  - 更新個別商品數量
  - 使用者登出時更新相關資料庫
- 評價功能
  - 購買後可以為商品撰寫評價
- 訂單管理
  - 檢視訂單
  - 回報訂單問題

## 網頁功能流程圖

__*備註: 實線箭頭：流程; 虛線箭頭：流程中包含更新資料庫*__

### 使用者功能

#### 註冊帳號

```mermaid
flowchart TB
    subgraph Register
        direction TB
        U[User] --"1. 申請帳號"--> R[Register] -."2. 建立用戶 (尚未啟用)".-> UB[(UserBase)]
        
        R --"2. 寄出帳號啟用信"--> M[Mail] --> A[Activate] -."3. 用戶啟用".-> UB --"4. 用戶登入"--> L[Login] --> P[Profile page]
    end

    subgraph Address
        A -."3. 建立用戶地址".-> Ad[(Address)]
    end
```

#### 更改密碼、刪除用戶、更新資訊

```mermaid
flowchart
    subgraph ResetPassword
        direction TB
        U[User] --"R1. 申請帳號"--> PR[Password reset]
        PR --"R2. 寄出密碼更改信"--> M[Mail] --> A[Activate] --"R3. 建立新密碼"--> UB[(UserBase)]
    end
    subgraph UserProfile
        U --"更新資訊(E)、刪除帳號(D)"--> P[Profile]
    end
    P  --"D1. 用戶變更為非啟用狀態"--> UB 
    P --"E1. 更新用戶資訊"--> Ad[(Address)]
    P --"E1. 更新用戶資訊"--> UB
```

### 購物袋

```mermaid
flowchart LR
    subgraph Store
        P[Prodcut] 
    end
    subgraph WishList
        W[Wish List]
    end
    subgraph ShoppingBag
        B[Shopping Bag] --"2. 在Session 中寫入購物袋訊息"--> B
        W --"1. 加入購物袋"--> B
        P --"1. 加入購物袋" --> B --> LS{Login Status}
        LS --"Yes"--> LO[Logout] -."3. 將Session中資料更新至Database".-> BD[(Shopping Bag)]
        LS --"No"--> LE[Leave] --> R[Clean Data in Session when user leave]
    end


```

願望清單:

1. 新增更新願望清單
2. 將願望清單商品加入購物袋(數量為1)

結帳:

1. 選取寄送方式
2. 更新寄送地址
3. Paypal 付款

訂單與評價

1. 付款完成後會建立訂單，可以在訂單頁面查詢訂單
2. 回報訂單問題
3. 連結並評價商品

## 需求

---
