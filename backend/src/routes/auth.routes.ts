import { Router } from "express";
import { AuthController } from "../controllers/auth.controller";

const router = Router();
const authController = new AuthController();

// Health check
router.get("/health", (req, res) => {
  res.json({ status: "ok", message: "Auth service is running" });
});

// Public routes
router.post("/register", (req, res) => authController.register(req, res));
router.post("/login", (req, res) => authController.login(req, res));

// ⚠️ "Protected" routes (not actually protected in Phase 1)
router.get("/profile/:id", (req, res) => authController.getProfile(req, res));
router.get("/users", (req, res) => authController.getAllUsers(req, res));

export default router;
