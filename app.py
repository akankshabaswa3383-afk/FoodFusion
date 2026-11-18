import streamlit as st
import sqlite3
import hashlib
import secrets
import hmac
from utils.ingredient_data import foods

# 2. DATABASE SYSTEM
def init_auth_db():
    conn = sqlite3.connect("foodfusion.db")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL COLLATE NOCASE,
            salt TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def hash_password(password, salt=None):
    if salt is None:
        salt = secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), salt.encode(), 200000
    ).hex()

    return salt, password_hash


def register_user(full_name, email, password):
    salt, password_hash = hash_password(password)

    try:
        conn = sqlite3.connect("foodfusion.db")
        conn.execute("""
            INSERT INTO users
            (full_name, email, salt, password_hash)
            VALUES (?, ?, ?, ?)
        """, (full_name, email, salt, password_hash))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False


def verify_user(email, password):
    conn = sqlite3.connect("foodfusion.db")
    conn.row_factory = sqlite3.Row

    user = conn.execute(
        "SELECT * FROM users WHERE email = ?", (email,)
    ).fetchone()

    conn.close()

    if user is None:
        return None

    _, password_hash = hash_password(password, user["salt"])

    if hmac.compare_digest(password_hash, user["password_hash"]):
        return dict(user)

    return None


init_auth_db()


# 3. YOUR EXISTING CSS STARTS HERE
st.markdown("""
<style>
/* Keep your existing CSS here */
</style>
""", unsafe_allow_html=True)


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="FoodFusion | Luxury Dining",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- THEME CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Poppins:wght@300;400;500;600;700&display=swap');

.stApp {
    background: #17191B;
    color: #F5F1E8;
    font-family: 'Poppins', sans-serif;
}

header, footer {visibility: hidden;}
.block-container {
    padding-top: 1rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

section[data-testid="stSidebar"] {
    background: #101112;
}

h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: #E9B949 !important;
}

p, label, span, div {
    font-family: 'Poppins', sans-serif;
}

.gold-text { color: #E9B949; }
.small-heading {
    color: #E9B949;
    font-size: 13px;
    letter-spacing: 2px;
    font-weight: 600;
    text-transform: uppercase;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    color: #F3BD4E;
    font-size: clamp(36px, 5vw, 58px);
    line-height: 1.13;
    font-weight: 800;
    margin: 15px 0;
}

.hero-description {
    color: #D0D0D0;
    font-size: 15px;
    line-height: 1.9;
}

.brand {
    font-family: 'Playfair Display', serif;
    font-size: 30px;
    font-weight: 800;
    color: #F4F0E7;
}

.brand span { color: #E9B949; }

div.stButton > button {
    background: #E9A817;
    color: #171717;
    border: 1px solid #E9A817;
    border-radius: 7px;
    padding: 10px 22px;
    font-weight: 700;
    transition: 0.3s;
}

div.stButton > button:hover {
    background: transparent;
    color: #E9B949;
    border: 1px solid #E9B949;
}

div[data-testid="stRadio"] > div {
    gap: 10px;
}

div[data-testid="stRadio"] label {
    color: #EAEAEA !important;
    font-size: 13px;
}

div[data-testid="stRadio"] label:hover {
    color: #E9B949 !important;
}

div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input,
div[data-testid="stTextArea"] textarea {
    background: #242629;
    color: #FFFFFF;
    border: 1px solid #55504A;
    border-radius: 7px;
}

div[data-testid="stSelectbox"] div[data-baseweb="select"] {
    background: #242629;
    color: white;
}

.food-card {
    background: #222528;
    border: 1px solid #45413A;
    border-radius: 12px;
    padding: 14px;
    margin-bottom: 20px;
    min-height: 145px;
}

.food-card h3 {
    font-size: 21px;
    margin-bottom: 5px;
}

.food-card p {
    color: #C7C7C7;
    font-size: 13px;
    line-height: 1.6;
}

.price {
    color: #E9B949;
    font-size: 19px;
    font-weight: 700;
}

.feature-card {
    background: #222528;
    border: 1px solid #49443B;
    padding: 22px;
    border-radius: 12px;
    min-height: 155px;
}

.feature-card h3 {
    font-size: 20px;
}

.feature-card p {
    color: #C9C9C9;
    font-size: 13px;
    line-height: 1.7;
}

hr {
    border-color: #45413A;
}

div[data-testid="stAlert"] {
    background: #292722;
    color: #F5F1E8;
}

</style>
""", unsafe_allow_html=True)


# ---------------- FOOD DATA ----------------

foods = [
    {
        "name": "Classic Cheese Burger",
        "category": "Fast Food",
        "price": 199,
        "description": "Juicy burger with cheese and fresh vegetables.",
        "image": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=700",
        "ingredients": "Burger bun, chicken patty, cheese, lettuce, tomato, onion, mayonnaise.",
        "recipe": "1. Cook the patty until fully cooked.\n2. Toast the burger buns.\n3. Add lettuce, tomato and onion.\n4. Place the patty and cheese inside.\n5. Add mayonnaise and serve."
    },
    {
        "name": "Margherita Pizza",
        "category": "Pizza",
        "price": 249,
        "description": "Classic Italian pizza with cheese and tomato.",
        "image": "https://images.unsplash.com/photo-1579751626657-72bc17010498?w=700",
        "ingredients": "Pizza base, tomato sauce, mozzarella cheese, basil, olive oil.",
        "recipe": "1. Spread tomato sauce over the pizza base.\n2. Add mozzarella cheese.\n3. Add fresh basil leaves.\n4. Bake until the crust is golden and cheese melts.\n5. Serve hot."
    },
    {
        "name": "Chicken Biryani",
        "category": "Indian",
        "price": 249,
        "description": "Traditional aromatic chicken biryani.",
        "image": "https://images.unsplash.com/photo-1563379091339-03246963d96c?w=700",
        "ingredients": "Basmati rice, chicken, onion, tomato, curd, ginger-garlic paste, biryani spices, mint.",
        "recipe": "1. Marinate chicken with curd and spices.\n2. Fry onions until golden.\n3. Cook chicken with tomatoes and spices.\n4. Add partially cooked basmati rice.\n5. Cook together until the rice and chicken are fully cooked."
    },
    {
        "name": "Fresh Garden Salad",
        "category": "Healthy",
        "price": 149,
        "description": "Fresh vegetables with a refreshing dressing.",
        "image": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=700",
        "ingredients": "Lettuce, cucumber, tomato, carrot, onion, lemon juice, olive oil.",
        "recipe": "1. Wash all vegetables.\n2. Chop cucumber, tomato and carrot.\n3. Add lettuce and onion.\n4. Mix lemon juice and olive oil.\n5. Toss everything and serve fresh."
    },
    {
        "name": "Creamy Alfredo Pasta",
        "category": "Italian",
        "price": 229,
        "description": "Creamy pasta with cheese and herbs.",
        "image": "https://images.unsplash.com/photo-1473093295043-cdd812d0e601?w=700",
        "ingredients": "Pasta, milk, cream, butter, garlic, parmesan cheese, black pepper.",
        "recipe": "1. Boil pasta until cooked.\n2. Melt butter in a pan.\n3. Add garlic, cream and milk.\n4. Mix in parmesan cheese.\n5. Add pasta and season with pepper."
    },
    {
        "name": "Grilled Salmon",
        "category": "Seafood",
        "price": 399,
        "description": "Grilled salmon with lemon and fresh herbs.",
        "image": "https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=700",
        "ingredients": "Salmon, lemon, garlic, olive oil, black pepper, herbs.",
        "recipe": "1. Season salmon with garlic, pepper and lemon.\n2. Brush with olive oil.\n3. Grill until thoroughly cooked.\n4. Add fresh herbs.\n5. Serve with lemon."
    },
    {
        "name": "Masala Dosa",
        "category": "Indian",
        "price": 99,
        "description": "Crispy South Indian dosa with potato masala.",
        "image": "https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=700",
        "ingredients": "Dosa batter, potato, onion, mustard seeds, curry leaves, turmeric.",
        "recipe": "1. Boil and mash potatoes.\n2. Prepare masala with onion and spices.\n3. Spread dosa batter on a hot pan.\n4. Cook until crispy.\n5. Add potato masala and fold."
    },
    {
        "name": "Chocolate Cake",
        "category": "Dessert",
        "price": 149,
        "description": "Soft chocolate cake with rich chocolate flavour.",
        "image": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=700",
        "ingredients": "Flour, cocoa powder, sugar, milk, eggs, butter, baking powder.",
        "recipe": "1. Mix flour, cocoa powder and baking powder.\n2. Add sugar, milk, eggs and butter.\n3. Mix into a smooth batter.\n4. Bake until cooked through.\n5. Cool and decorate with chocolate frosting."
    },
    {
        "name": "French Fries",
        "category": "Snacks",
        "price": 99,
        "description": "Golden crispy potato fries.",
        "image": "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=700",
        "ingredients": "Potatoes, salt, oil, black pepper, paprika.",
        "recipe": "1. Wash and cut potatoes into strips.\n2. Soak briefly in cold water.\n3. Dry the potato strips.\n4. Bake or fry until golden and cooked.\n5. Season with salt and pepper."
    },
    {
        "name": "Chicken Tacos",
        "category": "Mexican",
        "price": 189,
        "description": "Mexican tacos filled with seasoned chicken.",
        "image": "https://images.unsplash.com/photo-1551504734-5ee1c4a1479b?w=700",
        "ingredients": "Tortillas, chicken, lettuce, tomato, onion, cheese, salsa.",
        "recipe": "1. Season and cook chicken thoroughly.\n2. Warm the tortillas.\n3. Add lettuce and chopped tomatoes.\n4. Add chicken and cheese.\n5. Finish with salsa."
    },
    {
        "name": "Vegetable Fried Rice",
        "category": "Chinese",
        "price": 159,
        "description": "Fried rice with colourful vegetables.",
        "image": "https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=700",
        "ingredients": "Cooked rice, carrot, beans, capsicum, spring onion, soy sauce, garlic.",
        "recipe": "1. Prepare cooked and cooled rice.\n2. Sauté garlic and vegetables.\n3. Add cooked rice.\n4. Mix in soy sauce.\n5. Garnish with spring onion."
    },
    {
        "name": "Pancakes",
        "category": "Breakfast",
        "price": 139,
        "description": "Fluffy pancakes with maple syrup.",
        "image": "https://images.unsplash.com/photo-1528207776546-365bb710ee93?w=700",
        "ingredients": "Flour, milk, eggs, sugar, baking powder, butter, maple syrup.",
        "recipe": "1. Mix flour, sugar and baking powder.\n2. Add milk and eggs.\n3. Prepare a smooth batter.\n4. Cook small portions on a lightly buttered pan.\n5. Serve with maple syrup."
    },
    {
        "name": "Paneer Butter Masala",
        "category": "Indian",
        "price": 219,
        "description": "Paneer cubes in a rich tomato gravy.",
        "image": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=700",
        "ingredients": "Paneer, tomato, onion, butter, cream, ginger, garlic, Indian spices.",
        "recipe": "1. Prepare tomato and onion gravy.\n2. Add ginger, garlic and spices.\n3. Blend into a smooth sauce.\n4. Add paneer cubes, butter and cream.\n5. Simmer and serve with naan."
    },
    {
        "name": "Sushi Rolls",
        "category": "Japanese",
        "price": 299,
        "description": "Japanese-style rice rolls with fresh fillings.",
        "image": "https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=700",
        "ingredients": "Sushi rice, nori sheets, cucumber, avocado, rice vinegar.",
        "recipe": "1. Cook sushi rice and season with rice vinegar.\n2. Place nori on a sushi mat.\n3. Spread rice evenly.\n4. Add cucumber and avocado.\n5. Roll tightly and cut into pieces."
    },
    {
        "name": "Tomato Soup",
        "category": "Soup",
        "price": 109,
        "description": "Warm tomato soup with herbs.",
        "image": "https://images.unsplash.com/photo-1547592180-85f173990554?w=700",
        "ingredients": "Tomatoes, onion, garlic, butter, vegetable stock, pepper, herbs.",
        "recipe": "1. Cook tomatoes, onion and garlic.\n2. Add vegetable stock.\n3. Simmer until soft.\n4. Blend until smooth.\n5. Season and serve warm."
    },
    {
        "name": "Club Sandwich",
        "category": "Snacks",
        "price": 169,
        "description": "Triple-layer sandwich with fresh fillings.",
        "image": "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=700",
        "ingredients": "Bread, lettuce, tomato, cucumber, cheese, mayonnaise.",
        "recipe": "1. Toast bread slices.\n2. Spread mayonnaise.\n3. Layer lettuce, tomato and cucumber.\n4. Add cheese and another bread slice.\n5. Cut into triangles and serve."
    },
    {
        "name": "Veg Noodles",
        "category": "Chinese",
        "price": 159,
        "description": "Stir-fried noodles with fresh vegetables.",
        "image": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=700",
        "ingredients": "Noodles, cabbage, carrot, capsicum, soy sauce, garlic, spring onion.",
        "recipe": "1. Boil noodles until cooked.\n2. Sauté garlic and vegetables.\n3. Add noodles.\n4. Mix in soy sauce.\n5. Garnish with spring onion."
    },
    {
        "name": "Chocolate Brownie",
        "category": "Dessert",
        "price": 119,
        "description": "Rich chocolate brownie with a soft centre.",
        "image": "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=700",
        "ingredients": "Dark chocolate, flour, butter, sugar, eggs, cocoa powder.",
        "recipe": "1. Melt chocolate and butter.\n2. Mix in sugar and eggs.\n3. Add flour and cocoa powder.\n4. Pour into a baking tray.\n5. Bake and cool before cutting."
    },
    {
        "name": "Chicken Shawarma",
        "category": "Middle Eastern",
        "price": 199,
        "description": "Chicken wrap with garlic sauce and vegetables.",
        "image": "https://images.unsplash.com/photo-1529006557810-274b9b2fc783?w=700",
        "ingredients": "Chicken, pita bread, yogurt, garlic, lettuce, cucumber, garlic sauce.",
        "recipe": "1. Marinate chicken with yogurt and spices.\n2. Cook chicken thoroughly.\n3. Warm pita bread.\n4. Add chicken, lettuce and cucumber.\n5. Roll with garlic sauce."
    },
    {
        "name": "Strawberry Milkshake",
        "category": "Beverages",
        "price": 129,
        "description": "Creamy strawberry milkshake.",
        "image": "https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=700",
        "ingredients": "Strawberries, milk, vanilla ice cream, sugar.",
        "recipe": "1. Wash and prepare strawberries.\n2. Add strawberries and chilled milk to a blender.\n3. Add ice cream.\n4. Blend until smooth.\n5. Serve chilled."
    }
]


# ---------------- SESSION STATE ----------------
if "cart" not in st.session_state:
    st.session_state.cart = []

if "orders" not in st.session_state:
    st.session_state.orders = []


def add_to_cart(food):
    st.session_state.cart.append({
        "name": food["name"],
        "price": food["price"],
        "quantity": 1
    })


# ---------------- LOGIN AND REGISTER SYSTEM ----------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.logged_in:

    st.markdown("---")

    st.markdown(
        "<h1 style='text-align:center;'>Welcome to FoodFusion</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center;color:#E9B949;'>"
        "YOUR PREMIUM DINING EXPERIENCE STARTS HERE"
        "</p>",
        unsafe_allow_html=True
    )

    left, center, right = st.columns([1, 2, 1])

    with center:

        auth_choice = st.radio(
            "Account",
            ["Login", "Register"],
            horizontal=True
        )

        if auth_choice == "Register":

            st.subheader("Create Your Account")

            with st.form("register_form"):

                full_name = st.text_input("Full Name")
                email = st.text_input("Email Address")

                password = st.text_input(
                    "Password",
                    type="password"
                )

                confirm_password = st.text_input(
                    "Confirm Password",
                    type="password"
                )

                register = st.form_submit_button(
                    "Create Account",
                    use_container_width=True
                )

                if register:

                    if not all([
                        full_name.strip(),
                        email.strip(),
                        password,
                        confirm_password
                    ]):
                        st.error("Please fill in all fields.")

                    elif "@" not in email or "." not in email:
                        st.error("Enter a valid email address.")

                    elif len(password) < 8:
                        st.error("Password must contain at least 8 characters.")

                    elif password != confirm_password:
                        st.error("Passwords do not match.")

                    else:
                        success = register_user(
                            full_name.strip(),
                            email.strip(),
                            password
                        )

                        if success:
                            st.session_state.logged_in = True
                            st.session_state.username = full_name.strip()

                            st.success("Account created successfully!")
                            st.rerun()

                        else:
                            st.error(
                                "This email is already registered. Please log in."
                            )

        else:

            st.subheader("Login to Your Account")

            with st.form("login_form"):

                email = st.text_input("Email Address")

                password = st.text_input(
                    "Password",
                    type="password"
                )

                login = st.form_submit_button(
                    "Login",
                    use_container_width=True
                )

                if login:

                    if not email or not password:
                        st.error("Enter your email and password.")

                    else:
                        user = verify_user(
                            email.strip(),
                            password
                        )

                        if user:
                            st.session_state.logged_in = True
                            st.session_state.username = user["full_name"]

                            st.success("Login successful!")
                            st.rerun()

                        else:
                            st.error("Invalid email or password.")

    st.markdown("---")

    st.markdown(
        "<p style='text-align:center;color:#E9B949;'>"
        "✦ FoodFusion | Taste the Difference"
        "</p>",
        unsafe_allow_html=True
    )

    st.stop()

# ---------------- NAVIGATION ----------------
st.markdown("""
<div class="brand">✦ Food<span>Fusion</span></div>
<p style="color:#BDBDBD; font-size:11px; letter-spacing:3px;">
LUXURY DINING • EXCEPTIONAL EXPERIENCES
</p>
""", unsafe_allow_html=True)

st.markdown("---")

pages = [
    "Home",
    "About",
    "Menu",
    "Ingredient Checker",
    "Build Your Meal",
    "AI Recommendations",
    "ResQMeal",
    "Cart",
    "Orders",
]
def go_to_menu():
    st.session_state.navigation = "Menu"
page = st.radio(
    "Navigation",
    pages,
    horizontal=True,
    label_visibility="collapsed",
    key="navigation"
)

st.markdown("---")


# ---------------- HOME PAGE ----------------
if page == "Home":

    # USER PROFILE & LOGOUT

    col1, col2 = st.columns([4, 1])

    with col1:
        st.markdown(
            f"Welcome, **{st.session_state.username}**! ✨"
        )

    with col2:
        if st.button("🚪 Logout", key="home_logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()



    left, right = st.columns([1.1, 1])

    with left:
        st.markdown(
            '<div class="small-heading">EXPERIENCE THE BEST</div>',
            unsafe_allow_html=True
        )

        st.markdown("""
        <div class="hero-title">
        Indulge in<br>
        Luxurious Flavors
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="hero-description">
        Where every dish tells a story and every moment lingers.<br>
        Experience fine dining that captivates your senses.<br><br>
        Discover exceptional food, personalized meals and
        a smarter way to enjoy your dining experience.
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        st.button(
        "Explore Our Menu →",
        on_click=go_to_menu
    )

    with right:
        image1, image2 = st.columns(2)

        with image1:
            st.image(
                "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=700",
                use_container_width=True
            )

        with image2:
            st.write("")
            st.write("")
            st.image(
                "https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=700",
                use_container_width=True
            )

    st.write("")
    st.markdown("---")

    st.markdown(
        "<h2 style='text-align:center;'>The FoodFusion Experience</h2>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center;color:#C9C9C9;'>"
        "More than food. A personalized dining experience.</p>",
        unsafe_allow_html=True
    )

    st.write("")

# ---------------- ABOUT US PAGE ----------------

elif page == "About":

    # HERO SECTION
    st.markdown("""

        <p style="color:#E9B949;letter-spacing:3px;">
        DISCOVER FOODFUSION
        </p>

        <h1 style="
        font-family:Georgia;
        font-size:48px;
        color:#F2D58A;">
        Where Food Meets Innovation
        </h1>

        <p style="color:#E5E0D5;font-size:16px;">
        A smarter way to discover, customize and experience food
        through intelligent technology.
        </p>

    """, unsafe_allow_html=True)

    st.write("")

    # HERO IMAGE
    st.image(
        "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=1400",
        use_container_width=True
    )

    st.write("")

    # OUR STORY
    st.markdown(
        "<h2 style='color:#E9B949;'>✦ Our Story</h2>",
        unsafe_allow_html=True
    )

    left, right = st.columns([1.2, 1])

    with left:
        st.markdown("""
        <div style="
        background:#222528;
        padding:25px;
        border-radius:12px;
        border:1px solid #75602F;">

        <h3 style="color:#E9B949;">The Beginning of FoodFusion</h3>

        <p style="color:#E5E0D5;line-height:2;">
        FoodFusion was created with an idea of bringing food
        and technology together.

        We wanted to create more than an ordinary food ordering
        platform. Our goal is to make food discovery personalized,
        convenient and intelligent.

        By combining smart tools with a simple food experience,
        FoodFusion helps customers explore food in new ways.
        </p>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.image(
            "https://images.unsplash.com/photo-1556911220-bff31c812dba?w=800",
            use_container_width=True
        )

    st.write("")

    # MISSION AND VISION
    st.markdown(
        "<h2 style='color:#E9B949;'>✦ Our Mission & Vision</h2>",
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("""
        <div style="
        background:#24211C;
        border:1px solid #A98232;
        padding:25px;
        border-radius:12px;
        min-height:190px;">

        <h2>🎯 Our Mission</h2>

        <p style="color:#E5E0D5;line-height:1.8;">
        To make food ordering smarter and more convenient
        through personalization, intelligent recommendations
        and useful food technology.
        </p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div style="
        background:#24211C;
        border:1px solid #A98232;
        padding:25px;
        border-radius:12px;
        min-height:190px;">

        <h2>🌟 Our Vision</h2>

        <p style="color:#E5E0D5;line-height:1.8;">
        To create a connected food experience where
        technology makes discovering, preparing and
        enjoying food easier for everyone.
        </p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # WHAT MAKES US DIFFERENT
    st.markdown(
        "<h2 style='color:#E9B949;'>✦ What Makes FoodFusion Different?</h2>",
        unsafe_allow_html=True
    )

    st.write(
        "We combine several smart features into one food platform."
    )

    features = [
        (
            "🤖 AI-Powered Recommendations",
            "Discover food suggestions based on your preferences and budget."
        ),
        (
            "🥗 Smart Ingredient Checker",
            "Explore ingredients and identify common food allergens."
        ),
        (
            "👨‍🍳 Personalized Meal Builder",
            "Create customized meals using your favourite ingredients."
        ),
        (
            "♻️ Food Rescue Hub",
            "Discover discounted surplus meals and support food waste reduction."
        ),
        (
            "🍅 Pantry to Plate",
            "Discover recipe ideas using ingredients available at home."
        )
    ]

    for i in range(0, len(features), 3):

        cols = st.columns(3)

        for col, feature in zip(cols, features[i:i+3]):

            with col:

                st.markdown(f"""
                <div style="
                background:#222528;
                border:1px solid #75602F;
                border-radius:12px;
                padding:20px;
                min-height:170px;
                margin-bottom:15px;">

                <h3 style="color:#E9B949;font-size:18px;">
                {feature[0]}
                </h3>

                <p style="color:#D0D0D0;font-size:13px;line-height:1.8;">
                {feature[1]}
                </p>

                </div>
                """, unsafe_allow_html=True)

    st.write("")

   
    # CONTACT
    st.markdown(
        "<h2 style='color:#E9B949;'>✦ Get in Touch</h2>",
        unsafe_allow_html=True
    )

    st.write(
        "Have a suggestion or feedback? We would love to hear from you."
    )

    with st.form("about_feedback_form"):

        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        message = st.text_area("Your Feedback")

        submitted = st.form_submit_button("Send Feedback")

        if submitted:

            if name.strip() and email.strip() and message.strip():
                st.success("Thank you for sharing your feedback!")
            else:
                st.warning("Please complete all fields.")


# ---------------- FOOD MENU ----------------
elif page == "Menu":

    st.markdown('<div class="small-heading">DISCOVER OUR MENU</div>',
                unsafe_allow_html=True)
    st.title("Our Signature Dishes")
    st.write("Discover delicious dishes prepared for every taste.")

    search = st.text_input("🔍 Search for your favourite food")

    category = st.selectbox(
        "Choose a category",
        ["All", "Main Course", "Fast Food", "Healthy", "Dessert", "Snacks"]
    )

    filtered_foods = foods

    if category != "All":
        filtered_foods = [
            food for food in filtered_foods
            if food["category"] == category
        ]

    if search:
        filtered_foods = [
            food for food in filtered_foods
            if search.lower() in food["name"].lower()
        ]

    if not filtered_foods:
        st.warning("No matching dishes found.")

    for i in range(0, len(filtered_foods), 2):
        cols = st.columns(2)

        for col, food in zip(cols, filtered_foods[i:i + 2]):
            with col:
                st.image(food["image"], use_container_width=True)

                st.markdown(f"""
                <div class="food-card">
                    <h3>{food['name']}</h3>
                    <p>{food['description']}</p>
                    <p>{food['category']}</p>
                    <div class="price">₹{food['price']}</div>
                </div>
                """, unsafe_allow_html=True)

                with st.expander("📖 View Ingredients & Recipe"):

                    st.markdown("### 🥗 Ingredients")
                    st.write(food["ingredients"])

                    st.markdown("### 👨‍🍳 Preparation Method")
                    st.write(food["recipe"])


                if st.button(
                    f"Add {food['name']} to Cart",
                    key=f"add_{food['name']}"
                ):
                    add_to_cart(food)
                    st.success(f"{food['name']} added to cart!")



# ---------------- SMART INGREDIENT CHECKER ----------------
elif page == "Ingredient Checker":

    st.markdown(
        '<div class="small-heading">KNOW WHAT YOU EAT</div>',
        unsafe_allow_html=True
    )

    st.title("Smart Ingredient Checker")

    st.write(
        "Explore ingredients, recipes and common allergens "
        "in all our FoodFusion menu dishes."
    )

    # Connect all 20 menu items automatically
    food_names = [food["name"] for food in foods]

    selected_food = st.selectbox(
        "🍽️ Select a food item from our menu",
        food_names,
        key="ingredient_food_selector"
    )

    # Find selected food details
    food = next(
        item for item in foods
        if item["name"] == selected_food
    )

    st.markdown("---")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.image(food["image"], use_container_width=True)

    with col2:
        st.markdown(f"## {food['name']}")
        st.markdown(
            f"<div class='price'>₹{food['price']}</div>",
            unsafe_allow_html=True
        )
        st.write(food["description"])
        st.caption(f"Category: {food['category']}")

    st.markdown("---")

    # Ingredients
    st.subheader("🥗 Ingredients")

    st.info(food["ingredients"])

    # Common allergen keyword screening
    allergen_keywords = {
        "Milk": ["milk", "cheese", "butter", "cream", "paneer"],
        "Eggs": ["egg"],
        "Wheat / Gluten": ["wheat", "flour", "bread", "pasta",
                           "noodles", "bun", "tortilla"],
        "Peanuts": ["peanut"],
        "Soy": ["soy sauce", "soy"],
        "Fish": ["salmon"],
        "Sesame": ["sesame"]
    }

    ingredient_text = food["ingredients"].lower()

    detected = []

    for allergen, keywords in allergen_keywords.items():
        if any(word in ingredient_text for word in keywords):
            detected.append(allergen)

    st.subheader("⚠️ Common Allergen Check")

    if detected:
        for allergen in detected:
            st.warning(f"Possible {allergen} ingredient")
    else:
        st.success(
            "No listed common allergen keywords were detected."
        )

    st.caption(
        "This is a basic keyword screening tool, not an allergy safety "
        "guarantee. Check product labels and restaurant preparation "
        "details for cross-contact and hidden ingredients."
    )

    # Recipe
    st.markdown("---")

    st.subheader("👨‍🍳 Preparation Method")

    with st.expander("View Complete Recipe", expanded=True):
        st.write(food["recipe"])

    st.markdown("---")

    st.success(
        f"You are exploring {food['name']} from the FoodFusion menu!"
    )



# ---------------- BUILD YOUR OWN MEAL ----------------
elif page == "Build Your Meal":

    st.markdown(
        '<div class="small-heading">CREATE YOUR OWN DISH</div>',
        unsafe_allow_html=True
    )

    st.title("Build Your Own Meal")

    st.write(
        "Choose individual ingredients, mix your favourite flavours "
        "and create a personalized dish."
    )

    # Ingredient categories and prices
    ingredient_categories = {
        "🍚 Rice & Grains": {
            "Basmati Rice": 60,
            "Brown Rice": 70,
            "Fried Rice": 80,
            "Noodles": 70,
            "Pasta": 80
        },

        "🥕 Vegetables": {
            "Carrot": 20,
            "Broccoli": 35,
            "Capsicum": 25,
            "Onion": 15,
            "Tomato": 20,
            "Mushrooms": 40,
            "Sweet Corn": 30,
            "Cucumber": 20
        },

        "🧀 Dairy & Cheese": {
            "Paneer": 60,
            "Mozzarella Cheese": 45,
            "Cheddar Cheese": 45,
            "Cream": 30,
            "Butter": 20
        },

        "🍗 Protein": {
            "Chicken": 100,
            "Egg": 20,
            "Tofu": 60,
            "Salmon": 150
        },

        "🌿 Herbs & Spices": {
            "Garlic": 10,
            "Ginger": 10,
            "Black Pepper": 10,
            "Oregano": 10,
            "Chilli Flakes": 10,
            "Coriander": 10,
            "Mint": 10
        },

        "🥫 Sauces & Extras": {
            "Tomato Sauce": 20,
            "Soy Sauce": 15,
            "Mayonnaise": 20,
            "Chilli Sauce": 20,
            "Lemon Juice": 10
        }
    }

    selected_ingredients = []

    st.markdown("---")

    st.subheader("🥗 Choose Your Ingredients")

    for category, ingredients in ingredient_categories.items():

        with st.expander(category, expanded=True):

            ingredient_names = list(ingredients.keys())

            selected = st.multiselect(
                f"Select from {category}",
                ingredient_names,
                key=f"ingredients_{category}"
            )

            selected_ingredients.extend(selected)

    # ---------------- CALCULATE TOTAL ----------------

    total = sum(
        price
        for category in ingredient_categories.values()
        for name, price in category.items()
        if name in selected_ingredients
    )

    st.markdown("---")

    st.subheader("✨ Your Custom Dish")

    if selected_ingredients:

        st.write("### Selected Ingredients")

        for ingredient in selected_ingredients:
            st.write("✓", ingredient)

    else:
        st.info("Select ingredients to start creating your dish.")

    st.markdown("---")

    # ---------------- CUSTOMIZE YOUR RECIPE ----------------

    st.subheader("🎨 Customize Your Recipe")

    dish_name = st.text_input(
        "Name your dish",
        placeholder="My Special FoodFusion Dish"
    )

    cooking_style = st.selectbox(
        "Cooking style",
        ["Grilled", "Fried", "Boiled", "Baked", "Stir-fried"]
    )

    spice_level = st.selectbox(
        "Spice level",
        ["Mild", "Medium", "Spicy"]
    )

    portion = st.selectbox(
        "Portion size",
        ["Regular", "Large"]
    )

    # Calculate final price
    final_price = total * 1.2 if portion == "Large" else total

    st.markdown(
        f"<div class='price'>Estimated Total: ₹{final_price:.2f}</div>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    # ---------------- ADD CUSTOM MEAL TO CART ----------------

    if st.button(
        "🛒 Add My Meal to Cart",
        use_container_width=True
    ):

        if selected_ingredients:

            custom_meal = {
                "name": dish_name.strip() or "My Special Dish",
                "description": f"{cooking_style} | {spice_level} spice",
                "category": "Custom Meal",
                "price": final_price,
                "image": "",
                "ingredients": selected_ingredients.copy(),
                "quantity": 1
            }

            add_to_cart(custom_meal)

            st.success(
                "🎉 Your customized meal has been added to cart!"
            )

        else:
            st.warning(
                "Please select at least one ingredient."
            )



# ---------------- AI RECOMMENDATIONS ----------------

elif page == "AI Recommendations":

    from utils.ingredient_data import foods

    st.markdown(
        '<div class="small-heading">MADE FOR YOUR TASTE</div>',
        unsafe_allow_html=True
    )

    st.title("AI Food Recommendations")

    st.write(
        "Discover dishes based on your taste, budget and food preferences."
    )

    preference = st.selectbox(
        "Your food preference",
        [
            "All Food",
            "Vegetarian",
            "Non-Vegetarian",
            "Healthy Food",
            "Desserts",
            "Fast Food",
            "Indian Food",
            "Chinese Food",
            "Italian Food"
        ]
    )

    budget = st.selectbox(
        "Your budget",
        [
            "Any Budget",
            "Below ₹150",
            "₹150 - ₹250",
            "₹250 - ₹400",
            "Above ₹400"
        ]
    )

    search_ingredient = st.text_input(
        "Preferred ingredient (optional)",
        placeholder="Example: Paneer, Chicken, Cheese"
    )

    if st.button("✨ Get My Recommendations"):

        recommendations = []

        for food in foods:

            # Food preference filter
            category = food["category"].lower()

            ingredients = [
                ingredient.lower()
                for ingredient in food["ingredients"]
            ]

            if preference == "Vegetarian":
                if any(
                    item in ingredient
                    for ingredient in ingredients
                    for item in ["chicken", "salmon", "mutton", "fish"]
                ):
                    continue

            elif preference == "Non-Vegetarian":
                if not any(
                    item in ingredient
                    for ingredient in ingredients
                    for item in ["chicken", "salmon", "mutton", "fish"]
                ):
                    continue

            elif preference == "Healthy Food":
                if category != "healthy":
                    continue

            elif preference == "Desserts":
                if category != "desserts":
                    continue

            elif preference == "Fast Food":
                if category not in ["fast food", "snacks"]:
                    continue

            elif preference == "Indian Food":
                if category not in ["indian", "south indian", "north indian"]:
                    continue

            elif preference == "Chinese Food":
                if category != "chinese":
                    continue

            elif preference == "Italian Food":
                if category != "italian":
                    continue

            # Budget filter
            price = food["price"]

            if budget == "Below ₹150" and price >= 150:
                continue

            elif budget == "₹150 - ₹250" and not 150 <= price <= 250:
                continue

            elif budget == "₹250 - ₹400" and not 250 < price <= 400:
                continue

            elif budget == "Above ₹400" and price <= 400:
                continue

            # Ingredient filter
            if search_ingredient:
                if not any(
                    search_ingredient.lower().strip() in ingredient
                    for ingredient in ingredients
                ):
                    continue

            recommendations.append(food)

        st.markdown("---")

        st.subheader("✨ Recommended For You")

        if recommendations:

            st.success(
                f"We found {len(recommendations)} matching dishes!"
            )

            cols = st.columns(2)

            for i, food in enumerate(recommendations):

                with cols[i % 2]:

                    st.image(
                        food["image"],
                        use_container_width=True
                    )

                    st.markdown(f"### {food['name']}")

                    st.write(food["description"])

                    st.markdown(
                        f"**Price: ₹{food['price']}**"
                    )

                    st.caption(
                        "Ingredients: " +
                        ", ".join(food["ingredients"])
                    )

                    if st.button(
                        f"🛒 Add to Cart",
                        key=f"ai_recommend_{i}"
                    ):

                        add_to_cart(food)

                        st.success("Added to cart!")

        else:

            st.warning(
                "No matching dishes found. Try changing your preferences."
            )
# ---------------- RESQMEAL ----------------
elif page == "ResQMeal":

    st.markdown(
        '<div class="small-heading">SAVE FOOD • SHARE GOODNESS</div>',
        unsafe_allow_html=True
    )

    st.title("♻️ ResQMeal")
    st.subheader("Smart Food Rescue Hub")

    st.write(
        "Enjoy delicious meals at special discounted prices "
        "while helping reduce food waste."
    )

    st.markdown("---")

    # Sample surplus food listings
    rescue_foods = [
        {
            "name": "Vegetable Fried Rice",
            "original_price": 159,
            "rescue_price": 99,
            "discount": "38% OFF",
            "description": "Fresh vegetable fried rice with delicious spices.",
            "image": "https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=700"
        },
        {
            "name": "Classic Cheese Burger",
            "original_price": 199,
            "rescue_price": 129,
            "discount": "35% OFF",
            "description": "Cheesy burger with fresh vegetables.",
            "image": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=700"
        },
        {
            "name": "Masala Dosa",
            "original_price": 99,
            "rescue_price": 69,
            "discount": "30% OFF",
            "description": "Crispy dosa served with traditional chutney.",
            "image": "https://images.unsplash.com/photo-1668236543090-82eba5ee5976?w=700"
        },
        {
            "name": "Chocolate Cake",
            "original_price": 149,
            "rescue_price": 99,
            "discount": "34% OFF",
            "description": "Delicious chocolate cake for dessert lovers.",
            "image": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=700"
        }
    ]

    st.markdown(
        "### 🌱 Today's Food Rescue Deals"
    )

    for index, food in enumerate(rescue_foods):

        col1, col2 = st.columns([1, 2])

        with col1:
            st.image(
                food["image"],
                use_container_width=True
            )

        with col2:
            st.markdown(f"### {food['name']}")

            st.write(food["description"])

            st.markdown(
                f"""
                <p style="color:#E9B949;font-weight:bold;">
                    {food['discount']}
                </p>
                <p>
                    <span style="text-decoration:line-through;color:gray;">
                        ₹{food['original_price']}
                    </span>
                    <span style="color:#E9B949;font-size:24px;font-weight:bold;">
                        ₹{food['rescue_price']}
                    </span>
                </p>
                """,
                unsafe_allow_html=True
            )

            if st.button(
                "♻️ Rescue This Meal",
                key=f"rescue_{index}",
                use_container_width=True
            ):

                st.session_state.cart.append({
                    "name": food["name"],
                    "price": food["rescue_price"],
                    "quantity": 1
                })

                st.success(
                    f"{food['name']} added to your cart!"
                )

        st.markdown("---")

    st.markdown(
        """
        <div style="
            background-color:#242424;
            padding:20px;
            border-radius:12px;
            text-align:center;
        ">
            <h3 style="color:#E9B949;">
                🌍 Small Meals, Big Impact!
            </h3>
            <p style="color:#FFFFFF;">
                Save delicious food, enjoy special prices,
                and help reduce food waste.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
# ---------------- CART ----------------
elif page == "Cart":

    st.markdown('<div class="small-heading">YOUR SELECTION</div>',
                unsafe_allow_html=True)
    st.title("Your Shopping Cart")

    if not st.session_state.cart:
        st.info("Your cart is empty. Visit the Menu to add some delicious food.")
    else:
        total = 0

        for i, item in enumerate(st.session_state.cart):
            col1, col2, col3 = st.columns([3, 1, 1])

            with col1:
                st.write(f"**{item['name']}**")

            with col2:
                st.write(f"₹{item['price']}")

            with col3:
                if st.button("Remove", key=f"remove_{i}"):
                    st.session_state.cart.pop(i)
                    st.rerun()

            total += item["price"] * item["quantity"]

        st.markdown("---")
        st.markdown(f"## Total Amount: ₹{total}")

       
# ---------------- CHECKOUT & DELIVERY DETAILS ----------------

if page == "Cart":

    if st.button("🛵 Proceed to Checkout", use_container_width=True):

        if st.session_state.cart:
            st.session_state.checkout_open = True
            st.rerun()

        else:
            st.warning("Your cart is empty. Please add food first.")

if st.session_state.get("checkout_open", False):

    st.markdown("---")
    st.title("🚚 Delivery Details")
    st.write("Please enter your information to complete your order.")

    with st.form("delivery_details_form"):

        st.subheader("👤 Customer Information")

        customer_name = st.text_input("Full Name")
        phone = st.text_input("Mobile Number")

        st.subheader("📍 Delivery Address")

        address = st.text_area("House No., Street, Area")
        city = st.text_input("City")
        pincode = st.text_input("PIN Code")

        instructions = st.text_area(
            "Delivery Instructions (Optional)",
            placeholder="Example: Deliver near the main gate"
        )

        st.subheader("💳 Payment Method")

        payment_method = st.radio(
            "Choose Payment Method",
            ["Cash on Delivery", "UPI (Demo Only)"]
        )

        st.markdown("---")
        st.subheader(f"Total Amount: ₹{total}")

        confirm = st.form_submit_button(
            "✅ Confirm Order",
            use_container_width=True
        )

        if confirm:

            if not all([
                customer_name.strip(),
                phone.strip(),
                address.strip(),
                city.strip(),
                pincode.strip()
            ]):
                st.error("Please fill in all required fields.")

            elif not phone.isdigit() or len(phone) != 10:
                st.error("Enter a valid 10-digit mobile number.")

            elif not pincode.isdigit() or len(pincode) != 6:
                st.error("Enter a valid 6-digit PIN code.")

            else:
                st.session_state.orders.append({
                    "items": [
                        item["name"]
                        for item in st.session_state.cart
                    ],
                    "total": total,
                    "customer_name": customer_name,
                    "phone": phone,
                    "address": address,
                    "city": city,
                    "pincode": pincode,
                    "instructions": instructions,
                    "payment_method": payment_method
                })

                st.session_state.cart = []
                st.session_state.checkout_open = False

                st.success("🎉 Your order has been placed successfully!")
                st.balloons()


# ---------------- ORDERS ----------------
elif page == "Orders":

    # USER PROFILE & LOGOUT

    col1, col2 = st.columns([4, 1])

    with col1:
        st.markdown(
            f"Welcome, **{st.session_state.username}**! ✨"
        )

    with col2:
        if st.button("🚪 Logout", key="order_logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()


    st.markdown('<div class="small-heading">YOUR FOOD JOURNEY</div>',
                unsafe_allow_html=True)
    st.title("My Orders")

    if not st.session_state.orders:
        st.info("You have no orders yet.")
    else:
        for number, order in enumerate(st.session_state.orders, 1):
            st.markdown(f"""
            <div class="food-card">
                <h3>Order #{number}</h3>
                <p>{', '.join(order['items'])}</p>
                <div class="price">₹{order['total']}</div>
                <p>Status: Order placed</p>
            </div>
            """, unsafe_allow_html=True)



# ---------------- FOOTER ----------------
st.markdown("---")

st.markdown("""
<div style="text-align:center; padding:20px;">
    <div class="brand">✦ Food<span>Fusion</span></div>
    <p style="color:#BDBDBD; font-size:13px;">
    Experience the best. Taste the difference.
    </p>
    <p style="color:#8A8A8A; font-size:11px;">
    © 2026 FoodFusion | Luxury Dining Experience
    </p>
</div>
""", unsafe_allow_html=True)
