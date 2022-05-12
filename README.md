# Tsao Books 網路書店

![Website tour](readme_figures/Website_tour.gif)

## 簡介

此網站是後端練習網站，由 <b>Django</b> 框架開發的 <b>MTV</b> 架構網路書店。後端由 <b>Class-based views</b> 為主輔以 <b>Function-based views</b> 作為業務邏輯層(V)，搭配 <b>MySQL</b> 作為資料庫(M)；前端頁面(T)則以原生 <b>Django template</b> 為主，搭配 <b>Jquery(ajax)</b> 與 <b>CSS</b> 實作互動功能與排版。
<br>
<br>

## 套件

![Python](https://img.shields.io/badge/Python-3.8.5-blue) ![Django](https://img.shields.io/badge/Django-4.0.3-blue) ![mysql](https://img.shields.io/badge/mysqlclient-2.1.0-green) ![Paypal](https://img.shields.io/badge/paypalcheckoutserversdk-1.0.1-green) ![Pillow](https://img.shields.io/badge/Pillow-9.1.0-green) ![shortuuid](https://img.shields.io/badge/shortuuid-1.0.8-green)

## 網頁Demo

<https://stevetsaoch.pythonanywhere.com/>

*若你想獲得完整體驗，可以用下列帳戶測試。*

### 測試帳號

- 用戶：
  - User name: AllenDanvers
  - Password: qazxcv123

### 付款帳戶

- Paypal
  - Account: paypalpublic@paypal.com
  - Password: paypalpublic1

<br>

## 網站架構

```mermaid
flowchart LR
    subgraph Store[Store]
        direction TB
        I[Index] -.-> C[Category]
        C -.-> S
        I --1--> S[Single]
    end
    subgraph Bag
        direction RL
        S --2--> B[Shopping Bag]
        S -.-> W[Wishlist] 
        W -.-> B
    end

    subgraph Checkout
        B --3--> DS[Delivery Option]
        DS --4--> CA[Check Address]
        CA --5--> P[Paypal]
    end
    subgraph Orders
        P --6--> O[Order]
        O -.-> OI[Order issue]
    end
    subgraph Reviews
        O --7--> S -.-> R[Review]
    end    
```

__*備註: 實線箭頭：預設流程; 虛線箭頭：可選擇流程*__
<br>

## 資料庫架構

![Database Diagram](readme_figures/Databases_diagram.png)

連結: <https://dbdiagram.io/d/6253befa2514c979030773a2>

<br>

## 主要練習

- Django
  - Class-based views
    - Override method以符合業務需求
    - 以 REST 風格撰寫部分功能(購物袋、願望清單)
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

- Jquery
  - 首頁翻頁、更新商品數量與刪除商品
  - 即時顯示評論
  - 紀錄商品點擊數 (用於找出Bestsellers)

- CSS
  - 製作簡易動畫(指向選項時改變背景，選取後產生陰影特效等)
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

---

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

---

### 購物袋與願望清單

```mermaid
flowchart TB
    subgraph Store
        P[Prodcut] 
    end
    subgraph WishList
        W[Wish List]
        P --"加入願望清單"--> W
    end
    subgraph ShoppingBag
        B[Shopping Bag] --"2. 在Session 更新購物袋訊息"--> B
        W --"W1. 加入購物袋"--> B
        P --"P1. 加入購物袋" --> B --> LS{Login Status}
        LS --"Login"--> LO[Logout] -."3. 將Session中資料更新至Database".-> BD[(Shopping Bag)]
        LS --"Anonymous user"--> LE[Leave] --> R[Clean Data in Session when user leave]
    end
```

---

### 結帳

```mermaid
    flowchart RL
    subgraph UserInformation
        UB[(User Base)]
        Ad[(Address)]
    end
    subgraph ShoppingBag
        B[Shopping Bag]
    end
    subgraph Profile
        PF[Profile]
        PFE[Profile Edit Form]
    end
    subgraph ShoppingRoute
        B --"1. 選取寄送方法"--> D[Delivery Method]
        D --"2. 確認/編輯寄送資訊"--> C{Delivery Information Checking Page}
        C --"U1. 更新資訊"--> PFE
        C --"A1. 更新資訊"--> PFE
        C --"3. 登入Paypal"--> P[Paypal]
        P -."4. 結帳，前往訂單頁面".-> O[(Orders)]
    end
        PFE -."U2. 更新資料庫".-> UB
        PFE -."A2. 更新資料庫".-> Ad
        UB --"U3. 回到個人資訊頁面"--> PF 
        Ad --"A3. 回到個人資訊頁面"--> PF
        PF --"UA4. 前往購物袋結帳"--> B
    
```

---

### 訂單管理與商品評價

```mermaid
    flowchart RL
    subgraph Product
      direction TB
        P[Product]
    end
    subgraph Orders
      O[Order] --"P1. 前往商品頁面"--> P
      O -."O1. 儲存訂單問題".-> OS[(Order Issue Report)]
    end
    RL{Have Leave Review yet}
    subgraph Review
      P --"P2. 確認是否留過評價"--> RL -."No, P3. 評分與評價".-> R[(Review)]
      RL --"Yes, P3. 檢視頁面"--> P
    end
```
