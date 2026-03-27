# Authorization

## Role-Based Access Control (RBAC)

```javascript
// Define roles and permissions
const ROLES = {
  ADMIN: "admin",
  MANAGER: "manager",
  USER: "user",
};

const PERMISSIONS = {
  [ROLES.ADMIN]: ["read", "write", "delete", "manage_users"],
  [ROLES.MANAGER]: ["read", "write", "manage_team"],
  [ROLES.USER]: ["read"],
};

// Check permission middleware
const authorize = (requiredPermission) => {
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({ error: "Unauthorized" });
    }

    const userPermissions = PERMISSIONS[req.user.role];
    if (!userPermissions || !userPermissions.includes(requiredPermission)) {
      return res.status(403).json({ error: "Forbidden" });
    }

    next();
  };
};

// Usage
app.delete("/users/:id", authenticate, authorize("delete"), (req, res) => {
  res.json({ message: "User deleted" });
});

// Check role middleware
const requireRole = (role) => {
  return (req, res, next) => {
    if (req.user?.role !== role) {
      return res.status(403).json({ error: "Forbidden" });
    }
    next();
  };
};

app.get("/admin/dashboard", authenticate, requireRole("admin"), (req, res) => {
  res.json({ message: "Admin dashboard" });
});
```

## Permission-Based Access

```javascript
// Store permissions in database
const userPermissions = await UserPermission.find({ userId: req.user.id });
const permissions = userPermissions.map((p) => p.permission);

// Check if user has permission
const hasPermission = (user, permission) => {
  return user.permissions?.includes(permission);
};

// Middleware
const checkPermission = (permission) => {
  return async (req, res, next) => {
    const user = await User.findById(req.user.id).populate("permissions");
    if (!hasPermission(user, permission)) {
      return res.status(403).json({ error: "Forbidden" });
    }
    next();
  };
};

// Usage
app.post("/posts", checkPermission("create_post"), (req, res) => {
  res.json({ message: "Post created" });
});
```

## Resource-Based Access Control

```javascript
// Check if user owns resource
const checkResourceOwnership = async (req, res, next) => {
  const resource = await Post.findById(req.params.id);

  if (resource.userId !== req.user.id && req.user.role !== "admin") {
    return res.status(403).json({ error: "Forbidden" });
  }

  req.resource = resource;
  next();
};

app.put("/posts/:id", authenticate, checkResourceOwnership, (req, res) => {
  res.json({ message: "Post updated" });
});

// Check if user can access resource
const canAccessResource = async (req, res, next) => {
  const resource = await Document.findById(req.params.id);

  const hasAccess =
    resource.userId === req.user.id ||
    resource.sharedWith.includes(req.user.id) ||
    req.user.role === "admin";

  if (!hasAccess) {
    return res.status(403).json({ error: "Forbidden" });
  }

  next();
};
```

## Attribute-Based Access Control (ABAC)

```javascript
// Define policies
const policies = [
  {
    resource: "post",
    action: "read",
    condition: (user, resource) => {
      return resource.public || resource.userId === user.id;
    },
  },
  {
    resource: "post",
    action: "delete",
    condition: (user, resource) => {
      return resource.userId === user.id || user.role === "admin";
    },
  },
];

// Check access
const checkAccess = (resource, action) => {
  return async (req, res, next) => {
    const policy = policies.find(
      (p) => p.resource === resource && p.action === action
    );

    if (!policy) {
      return res.status(404).json({ error: "Not found" });
    }

    const resourceData = await getResource(req.params.id);
    if (!policy.condition(req.user, resourceData)) {
      return res.status(403).json({ error: "Forbidden" });
    }

    next();
  };
};

app.get("/posts/:id", authenticate, checkAccess("post", "read"), (req, res) => {
  res.json(req.resource);
});
```

## Audit Logging

```javascript
// Log access attempts
const auditLog = async (userId, action, resource, allowed) => {
  await AuditLog.create({
    userId,
    action,
    resource,
    allowed,
    timestamp: new Date(),
    ip: req.ip,
  });
};

// Middleware
const logAccess = async (req, res, next) => {
  const originalJson = res.json;

  res.json = function (data) {
    const allowed = res.statusCode < 400;
    auditLog(req.user?.id, req.method, req.path, allowed);
    return originalJson.call(this, data);
  };

  next();
};

app.use(logAccess);
```
