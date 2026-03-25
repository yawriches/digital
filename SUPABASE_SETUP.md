# Supabase Database Setup Guide

## Step-by-Step Instructions to Create Your Database

### 1. Access Supabase Dashboard

1. Go to https://supabase.com
2. Sign in to your account
3. Select your project: **dpzlrpplqtlcuhvuoovt**
4. You should see your project dashboard

### 2. Open SQL Editor

1. In the left sidebar, click **"SQL Editor"**
2. Click **"New query"** button (top right)

### 3. Create Database Tables

1. **Copy the entire contents** of `supabase_schema.sql`
2. **Paste** into the SQL Editor
3. Click **"Run"** button (or press Ctrl+Enter)
4. You should see: ✅ **Success. No rows returned**
5. Check the messages - you should see:
   ```
   Database schema created successfully!
   Tables created: users, categories, products, cart_items, orders, order_items
   ```

### 4. Seed the Database with Sample Data

1. Click **"New query"** again
2. **Copy the entire contents** of `supabase_seed.sql`
3. **Paste** into the SQL Editor
4. Click **"Run"** button
5. You should see: ✅ **Success**
6. Check the messages - you should see:
   ```
   Database seeded successfully!
   Created:
   - 2 users (admin@smartwatches.com / admin123, john@example.com / password123)
   - 4 categories
   - 8 products
   ```

### 5. Verify Tables Were Created

1. In the left sidebar, click **"Table Editor"**
2. You should see these tables:
   - ✅ users
   - ✅ categories
   - ✅ products
   - ✅ cart_items
   - ✅ orders
   - ✅ order_items

3. Click on **"products"** table
4. You should see 8 products listed

### 6. Get Your Database Connection String

1. Click **"Project Settings"** (gear icon in left sidebar)
2. Click **"Database"** in the settings menu
3. Scroll to **"Connection string"**
4. Select **"URI"** tab
5. Copy the connection string - it looks like:
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.dpzlrpplqtlcuhvuoovt.supabase.co:5432/postgres
   ```
6. **Important:** Replace `[YOUR-PASSWORD]` with your actual database password
7. **URL-encode special characters** in the password:
   - `!` becomes `%21`
   - `$` becomes `%24`
   - `@` becomes `%40`
   - `#` becomes `%23`

### 7. Update Render Environment Variables

1. Go to your Render dashboard
2. Click on your **"smartwatches-ecommerce"** service
3. Go to **"Environment"** tab
4. Find or add **"DATABASE_URL"**
5. Paste your Supabase connection string (with URL-encoded password)
6. Click **"Save Changes"**
7. Render will automatically redeploy

---

## Your Database Credentials

**Supabase Project:** dpzlrpplqtlcuhvuoovt  
**Database Host:** db.dpzlrpplqtlcuhvuoovt.supabase.co  
**Database Port:** 5432  
**Database Name:** postgres  
**Database User:** postgres  

**Connection String Format:**
```
postgresql://postgres:[PASSWORD]@db.dpzlrpplqtlcuhvuoovt.supabase.co:5432/postgres
```

**Example with URL-encoded password (K9!vQ$7m@R2zL#4tX):**
```
postgresql://postgres:K9%21vQ%247m%40R2zL%234tX@db.dpzlrpplqtlcuhvuoovt.supabase.co:5432/postgres
```

---

## Test Accounts Created

### Admin Account
- **Email:** admin@smartwatches.com
- **Password:** admin123
- **Access:** Full admin panel access

### Customer Account
- **Email:** john@example.com
- **Password:** password123
- **Access:** Regular customer access

---

## Database Tables Overview

### users
Stores customer and admin accounts
- id, email, password_hash, first_name, last_name, phone, is_admin

### categories
Product categories (Smart Watches, Fitness Trackers, etc.)
- id, name, slug, description, is_active

### products
All smart watch products
- id, name, slug, description, price, stock, sku, category_id, images, etc.

### cart_items
Shopping cart items for logged-in users
- id, user_id, product_id, quantity

### orders
Customer orders
- id, order_number, user_id, total_amount, status, payment_status, shipping info

### order_items
Individual items in each order
- id, order_id, product_id, product_name, price, quantity, subtotal

---

## Troubleshooting

### Error: "relation already exists"
**Solution:** Tables already exist. Either:
- Skip the schema creation step
- Or drop tables first by running the DROP statements at the top of `supabase_schema.sql`

### Error: "permission denied"
**Solution:** Make sure you're using the correct database password and have proper permissions

### Error: "could not translate host name"
**Solution:** Check your internet connection and verify the Supabase host is correct

### Tables created but empty
**Solution:** Run the `supabase_seed.sql` script to populate with sample data

### Password authentication failed
**Solution:** 
1. Verify your database password in Supabase settings
2. Make sure special characters are URL-encoded
3. Use the exact connection string from Supabase dashboard

---

## Next Steps

1. ✅ Create tables in Supabase (run `supabase_schema.sql`)
2. ✅ Seed database (run `supabase_seed.sql`)
3. ✅ Update Render DATABASE_URL environment variable
4. ✅ Redeploy your Render service
5. ✅ Test your live website!

Your Smart Watches e-commerce database is now ready in Supabase! 🎉
