"use client";

import { useState } from "react"
import styles from "./page.module.css";
import React from "react";

export default function Home() {
  const [serverUrl, setServerUrl] = useState("https://qammmq2ddr.us-east-1.awsapprunner.com");
  const [inputText, setInputText] = useState("");
  const [status, setStatus] = useState("Ready");
  const [volume, setVolume] = useState(50);
  const [personality, setPersonality] = useState("normal");

  const personalities = [
    "normal",
    "excited",
    "depressed",
    "sassy",
    "strange",
    "shakespere",
    "beavis",
  ];

  const handleCommand = async (endpoint: string, formData: FormData) => {
    setStatus("Sending...");
    try {
      const res = await fetch(`${serverUrl}${endpoint}`, {
        method: "POST",
        body: formData,
      });
      if (res.ok) {
        setStatus("Success");
        setTimeout(() => setStatus("Ready"), 3000);
      } else {
        setStatus("Error: " + res.statusText);
      }
    } catch (error) {
      console.error(error);
      setStatus("Connection to Server Failed");
    }
  };

  const sendMotorCommand = (action: string) => {
    const data = new FormData();
    data.append("action", action);
    handleCommand("/control_fish", data);
  };

  const sendSpeakCommand = () => {
    if (!inputText) return;
    const data = new FormData();
    data.append("user_text", inputText);
    data.append("personality", personality);
    handleCommand("/generate_query", data);
    setInputText("");
  }

  const handleVolumeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newVol = parseInt(e.target.value);
    setVolume(newVol);
    const data = new FormData();
    data.append("level", newVol.toString());
    handleCommand("/set_volume", data);
  };

  return (
    <div className={styles.page}>
      <main className={styles.main}>
        <div className={styles.header}>
          <h1>FishAI Controller</h1>
          <div className={styles.connection}>
            <input
              type="text"
              value={serverUrl}
              onChange={(e) => setServerUrl(e.target.value)}
              placeholder="Server URL (e.g. http://192.168.1.5:5000)"
            />
            <span className={`${styles.status} ${status !== 'Ready' ? styles.active : ''}`}>
              {status}
            </span>
          </div>
        </div>

        <div className={styles.grid}>
          {/* Movement Controls */}
          <section className={styles.card}>
            <h2>Movement</h2>
            <div className={styles.motorGrid}>
              <div className={styles.controlGroup}>
                <span>Head</span>
                <button onMouseDown={() => sendMotorCommand("move_head_out")}>Out</button>
                <button onMouseDown={() => sendMotorCommand("move_head_in")}>In</button>
              </div>
              <div className={styles.controlGroup}>
                <span>Mouth</span>
                <button onMouseDown={() => sendMotorCommand("move_mouth_out")}>Out</button>
                <button onMouseDown={() => sendMotorCommand("move_mouth_in")}>In</button>
              </div>
              <div className={styles.controlGroup}>
                <span>Tail</span>
                <button onMouseDown={() => sendMotorCommand("move_tail_out")}>Out</button>
                <button onMouseDown={() => sendMotorCommand("move_tail_in")}>In</button>
              </div>
            </div>
          </section>

          {/* Personality & Volume */}
          <section className={styles.card}>
            <h2>Settings</h2>
            <div className={styles.settingGroup}>
              <label>Personality</label>
              <select
                value={personality}
                onChange={(e) => setPersonality(e.target.value)}
              >
                {personalities.map(p => (
                  <option key={p} value={p}>{p.charAt(0).toUpperCase() + p.slice(1)}</option>
                ))}
              </select>
            </div>

            <div className={styles.settingGroup}>
              <label>Volume: {volume}%</label>
              <input
                type="range"
                min="0"
                max="100"
                value={volume}
                onChange={handleVolumeChange}
              />
            </div>
          </section>

          {/* Text to Speech */}
          <section className={`${styles.card} ${styles.fullWidth}`}>
            <h2>Speak</h2>
            <div className={styles.chatBox}>
              <textarea
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                placeholder="Type something for the fish to say..."
                rows={3}
              />
              <button onClick={sendSpeakCommand} disabled={!inputText}>
                Send to Fish
              </button>
            </div>
          </section>
        </div>
      </main>
    </div>
  );
}
