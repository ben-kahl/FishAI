"use client";

import { useEffect, useState, useRef } from "react"
import styles from "./page.module.css";
import React from "react";

type Message = {
  role: 'user' | 'fish';
  text: string;
}

export default function Home() {
  const [serverUrl, setServerUrl] = useState(process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:5000");
  const [inputText, setInputText] = useState("");
  const [status, setStatus] = useState("Ready");
  const [volume, setVolume] = useState(50);
  const [personality, setPersonality] = useState("normal");
  const [fishStatus, setFishStatus] = useState<any>(null);
  const [chatHistory, setChatHistory] = useState<Message[]>([]);

  const chatEndRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatHistory]);

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
        return await res.json();
      } else {
        setStatus("Error: " + res.statusText);
        return null;
      }
    } catch (error) {
      console.error(error);
      setStatus("Connection to Server Failed");
      return null;
    }
  };

  const sendMotorCommand = (action: string) => {
    const data = new FormData();
    data.append("action", action);
    handleCommand("/control_fish", data);
  };

  const sendSpeakCommand = async () => {
    if (!inputText) return;
    const userMsg = inputText;
    setChatHistory(prev => [...prev, { role: 'user', text: userMsg }]);

    const data = new FormData();
    data.append("user_text", inputText);
    data.append("personality", personality);
    const responseData = await handleCommand("/generate_query", data);
    if (responseData && responseData.response) {
      setChatHistory(prev => [...prev, { role: 'fish', text: responseData.response }]);
      setInputText("");
    }
  }

  const handleVolumeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newVol = parseInt(e.target.value);
    setVolume(newVol);
    const data = new FormData();
    data.append("level", newVol.toString());
    handleCommand("/set_volume", data);
  };

  const handlePersonalityChange = async (e: React.ChangeEvent<HTMLSelectElement>) => {
    const newPersonality = e.target.value;
    setPersonality(newPersonality);
    const data = new FormData();
    data.append("personality", newPersonality);

    await handleCommand("/set_personality", data);
  };

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const res = await fetch(`${serverUrl}/get_status`);
        if (res.ok) {
          const data = await res.json();
          setFishStatus(data);
        }
      } catch (e) {
        console.error("Status fetch failed", e);
        setFishStatus({ status: "offline" });
      }
    };

    // Poll every 10 seconds
    const interval = setInterval(fetchStatus, 10000);
    fetchStatus(); // Initial fetch
    return () => clearInterval(interval);
  }, [serverUrl]);

  const getTimeSince = (timestamp: number) => {
    const diff = Math.floor(Date.now() / 1000 - timestamp);
    return `${diff}s ago`;
  };

  return (
    <div className={styles.page}>
      <main className={styles.main}>
        {/* Header */}
        <div className={styles.header}>
          <h1>FishAI Controller</h1>
          <div className={styles.connection}>
            <input
              type="text"
              value={serverUrl}
              onChange={(e) => setServerUrl(e.target.value)}
              placeholder="Server URL"
            />
            <span className={`${styles.status} ${status !== 'Ready' ? styles.active : ''}`}>
              {status}
            </span>
          </div>
        </div>

        {/* Telemetry Status Panel */}
        <div className={styles.telemetryBox}>
          <section className={`${styles.card} ${styles.fullWidth}`}>
            <div className={styles.telemetryHeader}>
              <h2>System Status</h2>
              <span className={fishStatus?.status === 'online' ? styles.badgeOnline : styles.badgeOffline}>
                {fishStatus?.status === 'online' ? 'ONLINE' : 'OFFLINE'}
              </span>
            </div>
            {fishStatus?.status === 'online' && fishStatus.data && (
              <div className={styles.statsGrid}>
                <div className={styles.statBox}>
                  <span className={styles.statLabel}>CPU Load</span>
                  <span className={styles.statValue}>{fishStatus.data.cpu_usage}%</span>
                </div>
                <div className={styles.statBox}>
                  <span className={styles.statLabel}>Memory</span>
                  <span className={styles.statValue}>{fishStatus.data.memory_usage}%</span>
                </div>
                <div className={styles.statBox}>
                  <span className={styles.statLabel}>Temp</span>
                  <span className={styles.statValue}>{fishStatus.data.temperature}°C</span>
                </div>
                <div className={styles.statBox}>
                  <span className={styles.statLabel}>Last Heartbeat</span>
                  <span className={styles.statValue}>{getTimeSince(fishStatus.data.last_seen)}</span>
                </div>
              </div>
            )}
          </section>
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

          {/* Settings */}
          <section className={styles.card}>
            <h2>Settings</h2>
            <div className={styles.settingGroup}>
              <label>Personality</label>
              <select value={personality} onChange={handlePersonalityChange}>
                {personalities.map(p => (
                  <option key={p} value={p}>{p.charAt(0).toUpperCase() + p.slice(1)}</option>
                ))}
              </select>
            </div>
            <div className={styles.settingGroup}>
              <label>Volume: {volume}%</label>
              <input type="range" min="0" max="100" value={volume} onChange={handleVolumeChange} />
            </div>
          </section>

          {/* Chat Interface */}
          <section className={`${styles.card} ${styles.fullWidth}`}>
            <h2>Conversation</h2>

            <div className={styles.historyWindow}>
              {chatHistory.length === 0 ? (
                <p className={styles.emptyHistory}>Start chatting with the fish!</p>
              ) : (
                chatHistory.map((msg, idx) => (
                  <div key={idx} className={`${styles.message} ${msg.role === 'user' ? styles.userMsg : styles.fishMsg}`}>
                    <div className={styles.msgBubble}>
                      <span className={styles.msgRole}>{msg.role === 'user' ? 'You' : 'Fish'}</span>
                      <p>{msg.text}</p>
                    </div>
                  </div>
                ))
              )}
              <div ref={chatEndRef} />
            </div>

            <div className={styles.chatBox}>
              <textarea
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendSpeakCommand(); } }}
                placeholder="Type a message..."
                rows={2}
              />
              <button onClick={sendSpeakCommand} disabled={!inputText || status === "Sending..."}>
                Send
              </button>
            </div>
          </section>
        </div>
      </main>
    </div>
  );
}
