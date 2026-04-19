# ☕ Brothers Cafe - Table Management System
## Tirupattur | GSTIN: 23278537256752

A complete restaurant management system with:
- 🪑 Customer table selection
- 🍽️ Full menu with categories & images
- 🛒 Cart & order placement  
- 📊 Staff portal with real-time notifications
- 🧾 Bill generation with discounts
- 📱 QR code online payment support
- 📥 Excel export

---

## 🚀 Quick Setup

### Step 1: Install Python dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run database migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 3: Seed sample data (tables, menu, categories, admin)
```bash
python manage.py seed_data
```

### Step 4: Start the server
```bash
python manage.py runserver
```

---

## 🌐 URLs

| URL | Description |
|-----|-------------|
| http://localhost:8000/ | Customer table selection |
| http://localhost:8000/staff/ | Staff portal |
| http://localhost:8000/admin/ | Django admin panel |

---

## 🔑 Default Login

- **Admin / Staff**: `admin` / `admin123`

---

## 📱 Customer Flow

1. **Select Table** → Choose an available table
2. **Browse Menu** → Filter by category, search items
3. **Add to Cart** → Select quantity for each item
4. **Place Order** → Enter name, phone, special instructions
5. **Track Order** → Real-time status updates
6. **View Bill** → Once completed by staff, pay online or offline
7. **Download Bill** → Excel format download

---

## 👨‍🍳 Staff Portal Flow

1. **Login** → Use staff/admin credentials
2. **Dashboard** → See pending, active, completed orders
3. **Order Actions**:
   - Accept → Preparing → Ready → Complete & Bill
4. **Complete Order** → Select discount % and payment method
5. **Table View** → See all table statuses
6. **Export Excel** → Daily or all-time order reports

---

## ⚙️ Django Admin Features

### Tables
- Add/edit tables (number, name, capacity, description)
- View status (available/occupied/reserved)

### Menu
- Add categories with emoji icons
- Add menu items with **images**, price, type (veg/nonveg/beverage)
- Toggle availability, mark as featured

### Shop Settings
- Update shop name, location, GSTIN
- Upload UPI QR code for online payments
- Set UPI ID

### Discounts
- Create discount offers (e.g. "Festival Offer - 21%")
- Toggle active/inactive
- Set validity dates

### Orders
- View all orders with status, payment info
- Export to Excel directly from admin

---

## 🗂️ Project Structure

```
brothers_cafe/
├── brothers_cafe/          # Django project settings
│   ├── settings.py
│   └── urls.py
├── restaurant/             # Main app
│   ├── models.py           # Database models
│   ├── views.py            # Business logic
│   ├── admin.py            # Admin configuration
│   ├── urls.py             # URL routing
│   ├── templates/          # HTML templates
│   │   └── restaurant/
│   │       ├── base.html
│   │       ├── table_selection.html  ← Customer landing
│   │       ├── menu.html             ← Menu & cart
│   │       ├── order_status.html     ← Order tracking
│   │       ├── bill.html             ← Bill & payment
│   │       ├── staff_portal.html     ← Staff dashboard
│   │       └── partials/
│   └── management/commands/
│       └── seed_data.py    ← Sample data seeder
├── media/                  # Uploaded images (menu, QR)
├── requirements.txt
└── README.md
```

---

## 🎨 Features

### Customer Side
- Beautiful dark-theme table selection with status indicators
- Category-based menu with search
- Cart with quantity controls
- Apply discount during ordering
- Real-time order tracking with animated progress bar
- Bill with payment options (QR scan or cash)
- Downloadable bill in Excel format

### Staff Portal
- Real-time audio alerts for new orders (Web Audio API, no file needed)
- Color-coded order cards by status
- One-click status updates: Accept → Preparing → Ready → Complete
- Discount selection on completion
- Payment method selection (Online/Offline)
- Table availability overview
- Today's revenue and order stats
- Excel export (daily or all-time)

### Admin Panel
- Full CRUD for tables, categories, menu items
- Image upload for menu items
- QR code upload for UPI payments
- Discount management
- Color-coded order status
- Excel export action

---

## 💡 Tips

1. **Adding more tables**: Go to Admin → Tables → Add Table
2. **Adding menu items with images**: Admin → Menu Items → Add Item + upload image
3. **Setting up QR payment**: Admin → Shop Settings → Upload UPI QR code image
4. **Activating discounts**: Admin → Discounts → Check "Is Active"
5. **Creating staff accounts**: Admin → Users → Add User → set is_staff = True

---

Made with ❤️ for Brothers Cafe, Tirupattur
