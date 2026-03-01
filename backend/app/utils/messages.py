class Messages:
    class Generic:
        INTERNAL_ERROR = "Internal Server Error"

    class Validation:
        INVALID_DATA = "Invalid data"
        MISSING_LOGIN_CREDS = "Login (email or username) and password are required."
        INVALID_EMAIL = "Invalid email address."
        MIN_LENGTH_NAME = "The name must have at least 2 characters."
        MIN_LENGTH_USERNAME = "The username must have at least 3 characters."
        MIN_LENGTH_PASSWORD = "The password must have at least 6 characters."
        PRICE_GREATER_THAN_ZERO = "The price must be greater than zero."
        NEGATIVE_QUANTITY = "The quantity cannot be negative."
        NO_VALID_DATA_UPDATE = "No valid data provided for update."

    class Auth:
        INVALID_CREDENTIALS = "Invalid email, username, or password."
        LOGOUT_SUCCESS = "Logged out successfully."

    class User:
        NOT_FOUND_TITLE = "User not found."
        NOT_FOUND_DESC = "User with ID {} does not exist."
        EMAIL_CONFLICT = "This email is already registered."
        USERNAME_CONFLICT = "This username is already taken."
        FORBIDDEN_UPDATE = "Access denied. You can only update your own account."
        FORBIDDEN_DELETE = "Access denied. You can only delete your own account."

    class Product:
        NOT_FOUND_TITLE = "Product not found."
        NOT_FOUND_DESC = "Product with ID {} does not exist."
        FORBIDDEN_UPDATE = "Access denied. You can only modify your own products."
        FORBIDDEN_DELETE = "Access denied. You can only delete your own products."
        CREATE_QUEUED = "Product creation queued successfully."
        UPDATE_QUEUED = "Product update queued successfully."
        DELETE_QUEUED = "Product deletion queued successfully."
        IMAGE_NOT_FOUND = "Image not found."

    class Repository:
        ERR_SAVE_PRODUCT = "Error saving product to database."
        ERR_GET_PRODUCT_ID = "Error fetching product by ID."
        ERR_GET_PRODUCTS = "Error fetching products list."
        ERR_UPDATE_PRODUCT = "Error updating product in database."
        ERR_DELETE_PRODUCT = "Error deleting product from database."
        ERR_SAVE_USER = "Error saving user to database."
        ERR_GET_USER_ID = "Error fetching user by ID."
        ERR_GET_USER_EMAIL = "Error fetching user by email."
        ERR_GET_USER_USERNAME = "Error fetching user by username."
        ERR_GET_USER_CRED = "Error fetching user by login credential."
        ERR_GET_USERS = "Error fetching users list."
        ERR_UPDATE_USER = "Error updating user in database."
        ERR_DELETE_USER = "Error deleting user from database."
