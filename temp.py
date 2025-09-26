# AWS Credentials
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

# API Keys
STRIPE_API_KEY = "sk_test_26PHem9AhJZvU623DfE1x4sd"
GOOGLE_API_KEY = "AIzaSyDaGmWKa4JsXZ-HjGw47PIgGdWQdXoQlxY"
OPENAI_API_KEY = "sk-proj-1234567890abcdefghijklmnopqrstuvwxyz1234567890"

# Database URLs
DATABASE_URL = "postgresql://user:password123@db.example.com:5432/dbname"
MONGODB_URI = "mongodb://admin:secretpass@cluster0.mongodb.net/mydb?retryWrites=true"
MYSQL_URL = "mysql://root:mysecretpassword@localhost:3306/production_db"

# JWT Tokens
JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"

# GitHub Tokens
GITHUB_TOKEN = "ghp_1234567890abcdefghijklmnopqrstuvwxyz12"
GITHUB_PAT = "github_pat_11ABCDEFG0123456789_abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQR"

# Generic Secrets
API_SECRET = "abc123def456ghi789jkl012mno345pqr678stu901vwx234yz"
SECRET_KEY = "super-secret-key-that-should-not-be-exposed-2024"

# These should trigger entropy-based detection
high_entropy_string = "a8f5f167f44f4964e6c998dee827110c"
base64_secret = "dGhpc2lzYXNlY3JldGtleXRoYXRzaG91bGRiZWRldGVjdGVk"
hex_secret = "deadbeef1234567890abcdef1234567890abcdef1234567890abcdef"

# Configuration that might contain secrets
config = {
    "encryption_key": "f4e2a1b3c5d7e9f1a2b4c6d8e0f2a4b6",
    "signing_secret": "1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b"
}
