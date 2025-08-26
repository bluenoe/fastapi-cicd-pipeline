"""
Performance tests using Locust.
Tests API performance under load.
"""

from locust import HttpUser, task, between
import random
import string


class FastAPIUser(HttpUser):
    """Simulated user for performance testing."""
    
    wait_time = between(1, 3)  # Wait 1-3 seconds between requests
    
    def on_start(self):
        """Setup that runs when a user starts."""
        self.test_user_data = {
            "email": f"test_{self.generate_random_string()}@example.com",
            "username": f"user_{self.generate_random_string()}",
            "full_name": "Test User",
            "password": "testpassword123",
            "is_active": True
        }
        self.token = None
        self.user_id = None
        self.post_ids = []
        
        # Create user and login
        self.create_user()
        self.login()
    
    def generate_random_string(self, length=8):
        """Generate random string for unique usernames/emails."""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    
    def create_user(self):
        """Create a test user."""
        response = self.client.post("/api/v1/users/", json=self.test_user_data)
        if response.status_code == 201:
            user_data = response.json()
            self.user_id = user_data["id"]
    
    def login(self):
        """Login and get authentication token."""
        login_data = {
            "username": self.test_user_data["username"],
            "password": self.test_user_data["password"]
        }
        
        response = self.client.post("/api/v1/auth/token", data=login_data)
        if response.status_code == 200:
            token_data = response.json()
            self.token = token_data["access_token"]
    
    @property
    def auth_headers(self):
        """Get authorization headers."""
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}
    
    @task(3)
    def health_check(self):
        """Test health check endpoint (most frequent)."""
        self.client.get("/healthz")
    
    @task(2)
    def get_root(self):
        """Test root endpoint."""
        self.client.get("/")
    
    @task(2)
    def list_posts(self):
        """Test listing posts."""
        self.client.get("/api/v1/posts/")
    
    @task(1)
    def get_current_user(self):
        """Test getting current user info."""
        if self.token:
            self.client.get("/api/v1/auth/me", headers=self.auth_headers)
    
    @task(1)
    def create_post(self):
        """Test creating a post."""
        if self.token:
            post_data = {
                "title": f"Performance Test Post {self.generate_random_string()}",
                "content": "This is a performance test post content.",
                "published": random.choice([True, False])
            }
            
            response = self.client.post(
                "/api/v1/posts/", 
                json=post_data, 
                headers=self.auth_headers
            )
            
            if response.status_code == 201:
                post_data = response.json()
                self.post_ids.append(post_data["id"])
    
    @task(1)
    def get_specific_post(self):
        """Test getting a specific post."""
        if self.post_ids:
            post_id = random.choice(self.post_ids)
            self.client.get(f"/api/v1/posts/{post_id}")
    
    @task(1)
    def update_post(self):
        """Test updating a post."""
        if self.token and self.post_ids:
            post_id = random.choice(self.post_ids)
            update_data = {
                "title": f"Updated Post {self.generate_random_string()}",
                "published": random.choice([True, False])
            }
            
            self.client.put(
                f"/api/v1/posts/{post_id}",
                json=update_data,
                headers=self.auth_headers
            )
    
    @task(1)
    def get_user_profile(self):
        """Test getting user profile."""
        if self.token and self.user_id:
            self.client.get(f"/api/v1/users/{self.user_id}", headers=self.auth_headers)


class AdminUser(HttpUser):
    """Simulated admin user for testing admin operations."""
    
    wait_time = between(2, 5)
    
    def on_start(self):
        """Setup admin user."""
        self.admin_data = {
            "email": f"admin_{self.generate_random_string()}@example.com",
            "username": f"admin_{self.generate_random_string()}",
            "full_name": "Admin User",
            "password": "adminpassword123",
            "is_active": True
        }
        self.token = None
        
        # Create admin user and login
        self.create_admin_user()
        self.login()
    
    def generate_random_string(self, length=8):
        """Generate random string."""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    
    def create_admin_user(self):
        """Create an admin user."""
        response = self.client.post("/api/v1/users/", json=self.admin_data)
        # Note: In real scenario, admin status would be set separately
    
    def login(self):
        """Login admin user."""
        login_data = {
            "username": self.admin_data["username"],
            "password": self.admin_data["password"]
        }
        
        response = self.client.post("/api/v1/auth/token", data=login_data)
        if response.status_code == 200:
            token_data = response.json()
            self.token = token_data["access_token"]
    
    @property
    def auth_headers(self):
        """Get authorization headers."""
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}
    
    @task(3)
    def list_all_posts(self):
        """Test listing all posts including unpublished."""
        self.client.get("/api/v1/posts/?published_only=false")
    
    @task(2)
    def get_metrics(self):
        """Test metrics endpoint."""
        self.client.get("/metrics")
    
    @task(1)
    def list_users(self):
        """Test listing users (admin operation)."""
        if self.token:
            self.client.get("/api/v1/users/", headers=self.auth_headers)


class ApiStressTest(HttpUser):
    """High-frequency requests for stress testing."""
    
    wait_time = between(0.1, 0.5)  # Very short wait time
    
    @task(10)
    def rapid_health_checks(self):
        """Rapid health check requests."""
        self.client.get("/healthz")
    
    @task(5)
    def rapid_root_requests(self):
        """Rapid root endpoint requests."""
        self.client.get("/")
    
    @task(3)
    def rapid_post_listing(self):
        """Rapid post listing requests."""
        self.client.get("/api/v1/posts/")