import {
  getFirestore,
  doc,
  getDoc,
  setDoc,
  serverTimestamp,
} from "firebase/firestore";

const normalizeEmail = (email) => (email ? String(email).trim().toLowerCase() : "");

/**
 * Ensures a Firestore profile exists at users/{uid} and returns the latest profile.
 * This is the single source of truth for `isAdmin`.
 */
export async function ensureUserProfile(fbUser, overrides = {}) {
  if (!fbUser?.uid) throw new Error("Missing Firebase user uid");

  const db = getFirestore();
  const ref = doc(db, "users", String(fbUser.uid));

  const base = {
    id: String(fbUser.uid),
    email: normalizeEmail(fbUser.email || overrides.email || ""),
    displayName:
      overrides.displayName ||
      fbUser.displayName ||
      fbUser.email?.split("@")[0] ||
      "User",
    photoURL: overrides.photoURL || fbUser.photoURL || "",
  };

  const snap = await getDoc(ref);

  // Create on first login/register
  if (!snap.exists()) {
    await setDoc(
      ref,
      {
        ...base,
        isAdmin: false,
        createdAt: serverTimestamp(),
      },
      { merge: true }
    );
    const created = await getDoc(ref);
    return created.data();
  }

  // Keep basic profile fields fresh, but never flip isAdmin here.
  await setDoc(ref, { ...base, updatedAt: serverTimestamp() }, { merge: true });
  const updated = await getDoc(ref);
  return updated.data();
}

export async function getUserProfile(uid) {
  const db = getFirestore();
  const ref = doc(db, "users", String(uid));
  const snap = await getDoc(ref);
  return snap.exists() ? snap.data() : null;
}
