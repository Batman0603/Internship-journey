import React, { useEffect, useState, useRef } from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { authAPI as api } from '../api/authAPI';

// Module-level cache / in-flight promise to dedupe / cache verify requests
let verifyCache = null; // { data, ts }
let verifyInFlight = null; // Promise that resolves to parsed JSON data
const VERIFY_TTL = 5 * 1000; // 5 seconds cache

/**
 * ProtectedRoute
 * - Calls GET /api/auth/verify with axios and withCredentials:true so HttpOnly cookie is sent
 * - If not authenticated or role not allowed, redirects to /login
 * - Otherwise renders child routes using <Outlet />
 *
 * Props:
 * - allowedRoles?: string[]  (optional) list of allowed roles for this route
 */
const ProtectedRoute = ({ allowedRoles } = {}) => {
  const [checking, setChecking] = useState(true);
  const [allowed, setAllowed] = useState(false);
  const [userRole, setUserRole] = useState(null);

  // Simple in-memory cache / dedupe for verify calls to avoid duplicate requests
  // across mounts (React StrictMode can mount/unmount twice in dev).
  // Module-level variables share across component instances.
  // TTL keeps a recent successful verification for a short time.
  const isMountedRef = useRef(true);

  useEffect(() => {
    isMountedRef.current = true;
    return () => {
      isMountedRef.current = false;
    };
  }, []);

  useEffect(() => {
    let cancelled = false;

    const verify = async () => {
      try {
        // Use cached result or in-flight promise to deduplicate calls
        const now = Date.now();
        if (verifyCache && verifyCache.data && now - verifyCache.ts < VERIFY_TTL) {
          // use cached data
          const data = verifyCache.data;
          if (cancelled) return;
          handleVerifyResult(data);
          return;
        }

        if (!verifyInFlight) {
          verifyInFlight = api.get('/api/auth/verify')
            .then((data) => {
              verifyCache = { data, ts: Date.now() };
              verifyInFlight = null;
              return data;
            })
            .catch((e) => {
              verifyInFlight = null;
              throw e;
            });
        }

        const data = await verifyInFlight;
        if (cancelled) return;
        handleVerifyResult(data);
      } catch (err) {
        // Only log and set unauthenticated for real errors
        const name = err?.name || err?.constructor?.name;
        if (name === 'CanceledError' || name === 'AbortError') {
          return;
        }
        console.error('ProtectedRoute verify error:', err);
        if (!isMountedRef.current) return;
        setAllowed(false);
        setChecking(false);
      }
    };

    const handleVerifyResult = (data) => {
      const isAuth = !!data?.authenticated;
      const role = data?.user?.role;

      // store role for redirecting
      if (isMountedRef.current) setUserRole(role || null);

      if (!isMountedRef.current) return;

      if (!isAuth) {
        setAllowed(false);
        setChecking(false);
        return;
      }

      if (Array.isArray(allowedRoles) && allowedRoles.length > 0) {
        setAllowed(allowedRoles.includes(role));
      } else {
        setAllowed(true);
      }

      setChecking(false);
    };

    verify();

    return () => {
      cancelled = true;
    };
  }, [allowedRoles]);

  if (checking) {
    // you can replace this with a spinner component
    return null;
  }

  if (!allowed) {
    return <Navigate to="/login" replace />;
  }

  // If checks pass, render the child component (e.g., the dashboard).
  // The <Outlet /> component from react-router-dom renders the matched child route.
  return <Outlet />;
};

export default ProtectedRoute;
