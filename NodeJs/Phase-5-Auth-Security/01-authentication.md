# Authentication

## JWT (JSON Web Tokens)

```javascript
const jwt = require("jsonwebtoken");

// Create token
const token = jwt.sign(
  { userId: 123, email: "user@example.com" },
  process.env.JWT_SECRET,
  { expiresIn: "24h" }
);

// Verify token
try {
  const decoded = jwt.verify(token, process.env.JWT_SECRET);
  console.log(decoded); // { userId: 123, email: '...', iat, exp }
} catch (err) {
  console.error("Invalid token:", err.message);
}

// Decode without verification (unsafe)
const decoded = jwt.decode(token);
```

## JWT in Express

```javascript
// Middleware to verify JWT
const authenticateToken = (req, res, next) => {
  const authHeader = req.headers["authorization"];
  const token = authHeader && authHeader.split(" ")[1]; // Bearer TOKEN

  if (!token) {
    return res.status(401).json({ error: "Access token required" });
  }

  jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
    if (err) {
      return res.status(403).json({ error: "Invalid token" });
    }
    req.user = user;
    next();
  });
};

// Login endpoint
app.post("/login", async (req, res) => {
  const { email, password } = req.body;

  // Find user
  const user = await User.findOne({ email });
  if (!user) {
    return res.status(401).json({ error: "Invalid credentials" });
  }

  // Verify password
  const validPassword = await bcrypt.compare(password, user.password);
  if (!validPassword) {
    return res.status(401).json({ error: "Invalid credentials" });
  }

  // Generate token
  const token = jwt.sign(
    { userId: user.id, email: user.email },
    process.env.JWT_SECRET,
    { expiresIn: "24h" }
  );

  res.json({ token });
});

// Protected route
app.get("/profile", authenticateToken, (req, res) => {
  res.json({ user: req.user });
});
```

## Password Hashing

```javascript
const bcrypt = require("bcrypt");

// Hash password
const password = "myPassword123";
const hashedPassword = await bcrypt.hash(password, 10); // 10 salt rounds

// Verify password
const isValid = await bcrypt.compare(password, hashedPassword);
console.log(isValid); // true

// Registration
app.post("/register", async (req, res) => {
  const { email, password } = req.body;

  // Check if user exists
  const existing = await User.findOne({ email });
  if (existing) {
    return res.status(400).json({ error: "User already exists" });
  }

  // Hash password
  const hashedPassword = await bcrypt.hash(password, 10);

  // Create user
  const user = await User.create({
    email,
    password: hashedPassword,
  });

  res.status(201).json({ message: "User created" });
});
```

## Sessions & Cookies

```javascript
const session = require("express-session");
const cookieParser = require("cookie-parser");

// Setup session
app.use(cookieParser());
app.use(
  session({
    secret: process.env.SESSION_SECRET,
    resave: false,
    saveUninitialized: true,
    cookie: {
      secure: true, // HTTPS only
      httpOnly: true, // No JavaScript access
      maxAge: 24 * 60 * 60 * 1000, // 24 hours
    },
  })
);

// Login with session
app.post("/login", async (req, res) => {
  const { email, password } = req.body;
  const user = await User.findOne({ email });

  if (!user || !(await bcrypt.compare(password, user.password))) {
    return res.status(401).json({ error: "Invalid credentials" });
  }

  // Store in session
  req.session.userId = user.id;
  req.session.user = user;

  res.json({ message: "Logged in" });
});

// Check session
app.get("/profile", (req, res) => {
  if (!req.session.userId) {
    return res.status(401).json({ error: "Not authenticated" });
  }
  res.json({ user: req.session.user });
});

// Logout
app.post("/logout", (req, res) => {
  req.session.destroy((err) => {
    if (err) return res.status(500).json({ error: "Logout failed" });
    res.json({ message: "Logged out" });
  });
});
```

## OAuth 2.0

```javascript
const passport = require("passport");
const GoogleStrategy = require("passport-google-oauth20").Strategy;

// Configure Passport
passport.use(
  new GoogleStrategy(
    {
      clientID: process.env.GOOGLE_CLIENT_ID,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET,
      callbackURL: "/auth/google/callback",
    },
    async (accessToken, refreshToken, profile, done) => {
      // Find or create user
      let user = await User.findOne({ googleId: profile.id });
      if (!user) {
        user = await User.create({
          googleId: profile.id,
          email: profile.emails[0].value,
          name: profile.displayName,
        });
      }
      return done(null, user);
    }
  )
);

// Serialize user
passport.serializeUser((user, done) => {
  done(null, user.id);
});

passport.deserializeUser(async (id, done) => {
  const user = await User.findById(id);
  done(null, user);
});

// Routes
app.use(passport.initialize());
app.use(passport.session());

app.get(
  "/auth/google",
  passport.authenticate("google", { scope: ["profile", "email"] })
);

app.get(
  "/auth/google/callback",
  passport.authenticate("google", { failureRedirect: "/login" }),
  (req, res) => {
    res.redirect("/dashboard");
  }
);
```

## Multi-factor Authentication

```javascript
const speakeasy = require("speakeasy");
const QRCode = require("qrcode");

// Generate 2FA secret
app.post("/2fa/setup", authenticateToken, async (req, res) => {
  const secret = speakeasy.generateSecret({
    name: `MyApp (${req.user.email})`,
    issuer: "MyApp",
  });

  // Generate QR code
  const qrCode = await QRCode.toDataURL(secret.otpauth_url);

  res.json({
    secret: secret.base32,
    qrCode,
  });
});

// Verify 2FA token
app.post("/2fa/verify", authenticateToken, (req, res) => {
  const { token, secret } = req.body;

  const verified = speakeasy.totp.verify({
    secret,
    encoding: "base32",
    token,
    window: 2,
  });

  if (!verified) {
    return res.status(400).json({ error: "Invalid token" });
  }

  res.json({ message: "2FA enabled" });
});
```

## Token Refresh

```javascript
// Generate tokens
const generateTokens = (userId) => {
  const accessToken = jwt.sign({ userId }, process.env.JWT_SECRET, {
    expiresIn: "15m",
  });

  const refreshToken = jwt.sign({ userId }, process.env.REFRESH_TOKEN_SECRET, {
    expiresIn: "7d",
  });

  return { accessToken, refreshToken };
};

// Login
app.post("/login", async (req, res) => {
  const user = await authenticate(req.body);
  const { accessToken, refreshToken } = generateTokens(user.id);

  // Store refresh token in database
  await RefreshToken.create({ userId: user.id, token: refreshToken });

  res.json({ accessToken, refreshToken });
});

// Refresh access token
app.post("/refresh", (req, res) => {
  const { refreshToken } = req.body;

  try {
    const decoded = jwt.verify(refreshToken, process.env.REFRESH_TOKEN_SECRET);
    const { accessToken, refreshToken: newRefreshToken } = generateTokens(
      decoded.userId
    );

    res.json({ accessToken, refreshToken: newRefreshToken });
  } catch (err) {
    res.status(401).json({ error: "Invalid refresh token" });
  }
});
```
