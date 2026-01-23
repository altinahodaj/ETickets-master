"use strict";

const firebase = require("../db");
const User = require("../Models/User");
const firestore = firebase.firestore();

const getUsers = async (req, res, next) => {
  console.log("getUsers called");
  try {
    const users = await firestore.collection("users");
    console.log("Fetching users from firestore...");
    const data = await users.get();
    console.log("Firestore response received, count:", data.size);
    const usersList = [];

    if (data.empty) {
      console.log("No users in 'users' collection.");
      res.status(200).send([]); // Return empty array instead of 404
    } else {
      data.forEach((doc) => {
        const d = doc.data();
        const user = new User(
          d.id || d.uid || doc.id,
          d.accessToken || "",
          d.displayName || d.name || "User",
          d.email,
          d.photoURL || "",
          d.isAdmin || false
        );
        usersList.push(user);
      });
      res.status(200).send(usersList);
    }
  } catch (error) {
    console.error("Error in getUsers:", error);
    res.status(400).send(error.message);
  }
};

const getUser = async (req, res, next) => {
  try {
    const id = req.params.id;
    const user = await firestore.collection("users").doc(id);
    const data = await user.get();

    if (!data.exists) {
      res.status(404).send(`Could not find User with id: ${id}`);
    } else {
      res.status(200).send(data.data());
    }
  } catch (error) {
    res.status(400).send(error.message);
  }
};

const updateUser = async (req, res, next) => {
  try {
    const id = req.params.id;
    const data = req.body;
    const user = await firestore.collection("users").doc(id);
    const userData = await user.get();

    if (!userData.exists) {
      res.status(404).send(`Could not find User with id: ${id}`);
    } else {
      await user.update(data);
      res.status(200).send("User updated successfully!");
    }
  } catch (error) {
    res.status(400).send(error.message);
  }
};

const makeAdmin = async (req, res, next) => {
  try {
    const id = req.params.id;
    const user = await firestore.collection("users").doc(id);
    const userData = await user.get();
    if (!userData.exists) {
      res.status(404).send(`Could not find User with id: ${id}`);
    } else {
      await user.update({
        isAdmin: true,
      });

      const updated = await user.get();
      res.status(200).send(updated.data());
    }
  } catch (error) {
    console.log(error)
    res.status(400).send(error.message);
  }
};

const removeAdmin = async (req, res, next) => {
  try {
    const id = req.params.id;
    const user = await firestore.collection("users").doc(id);
    const userData = await user.get();
    if (!userData.exists) {
      res.status(404).send(`Could not find User with id: ${id}`);
    } else {
      await user.update({
        isAdmin: false,
      });

      const updated = await user.get();
      res.status(200).send(updated.data());
    }
  } catch (error) {
    console.log(error)
    res.status(400).send(error.message);
  }
};

const addUser = async (req, res, next) => {
  try {
    const data = req.body;

    if (!data || !data.id) {
      return res.status(400).send("User 'id' is required");
    }

    const docRef = firestore.collection("users").doc(String(data.id));
    const existing = await docRef.get();

    // Upsert: create if missing, otherwise merge updates
    if (existing.exists) {
      await docRef.set(data, { merge: true });
    } else {
      await docRef.set(data);
    }

    const saved = await docRef.get();
    res.status(201).send({
      message: existing.exists ? "User updated successfully!" : "User created successfully!",
      result: saved.data(),
    });
  } catch (error) {
    res.status(400).send(error.message);
  }
};

const deleteUser = async (req, res, next) => {
  try {
    const id = req.params.id;
    await firestore.collection("users").doc(id).delete();
    res.status(200).send("User deleted successfully!");
  } catch (error) {
    res.status(400).send(error.message);
  }
};

module.exports = {
  getUsers,
  getUser,
  updateUser,
  addUser,
  deleteUser,
  makeAdmin,
  removeAdmin,
};
