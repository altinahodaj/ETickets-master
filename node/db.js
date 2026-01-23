const firebase = require("firebase");
const config = require("./config");

let db;
try {
    console.log("Initializing Firebase with project:", config.firebaseConfig?.projectId);
    db = firebase.initializeApp(config.firebaseConfig);
    console.log("Firebase initialized successfully");
} catch (e) {
    console.error("Firebase initialization failed:", e.message);
    // Në rast dështimi, krijojmë një objekt boş për të shmangur crashes
    db = {
        firestore: () => ({
            collection: () => ({
                get: () => Promise.resolve({ empty: true, size: 0 }),
                doc: () => ({
                    get: () => Promise.resolve({ exists: false }),
                    set: () => Promise.resolve(),
                    update: () => Promise.resolve(),
                    delete: () => Promise.resolve()
                })
            })
        })
    };
}

module.exports = db;
