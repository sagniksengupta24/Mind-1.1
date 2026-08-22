'use client';

import { useState, useEffect, useRef } from 'react';
import Link from 'next/link';
import { Sidebar } from './chat/Sidebar';
import { Composer } from './chat/Composer';
import { MessageTurn } from './chat/MessageTurn';
import { Conversation, Message } from './chat/types';

export function ChatPage() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeId, setActiveId] = useState<string | null>(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string>();
  const [loadingHistory, setLoadingHistory] = useState(false);

  const threadRef = useRef<HTMLDivElement>(null);

  // Load sessions from Backend SessionStore on mount
  useEffect(() => {
    async function loadBackendSessions() {
      try {
        const res = await fetch('/api/sessions', { cache: 'no-store' });
        if (!res.ok) {
          throw new Error(`Failed to load sessions from server (${res.status})`);
        }
        const data = await res.json();
        const serverSessions: Array<{ id: string; title: string; updated_at?: string }> =
          data.sessions || [];

        if (serverSessions.length > 0) {
          const convos: Conversation[] = serverSessions.map((s) => ({
            id: s.id,
            title: s.title || 'Conversation',
            messages: [],
            updatedAt: s.updated_at ? new Date(s.updated_at).getTime() : Date.now(),
            backendSessionId: s.id,
          }));
          setConversations(convos);
          const firstId = convos[0].id;
          setActiveId(firstId);
          loadSessionMessages(firstId);
        } else {
          // No existing sessions on backend; create an initial placeholder
          const initialId = Date.now().toString();
          setConversations([
            {
              id: initialId,
              title: 'New conversation',
              messages: [],
              updatedAt: Date.now(),
            },
          ]);
          setActiveId(initialId);
        }
      } catch (err: any) {
        console.error('Failed to load backend sessions:', err);
        setError(
          'Backend service unavailable. Please verify the Mind API server is running on http://localhost:8765.'
        );
      }
    }

    loadBackendSessions();
  }, []);

  // Fetch full message history for an active session
  const loadSessionMessages = async (sessionId: string) => {
    setLoadingHistory(true);
    setError(undefined);
    try {
      const res = await fetch(`/api/sessions/${encodeURIComponent(sessionId)}`, {
        cache: 'no-store',
      });
      if (res.ok) {
        const data = await res.json();
        const rawMsgs: Array<{ role: string; content: string }> = data.messages || [];
        const formattedMsgs: Message[] = rawMsgs.map((m) => ({
          role: m.role === 'assistant' ? 'assistant' : 'user',
          content: m.content,
        }));

        setConversations((prev) =>
          prev.map((c) => (c.id === sessionId ? { ...c, messages: formattedMsgs } : c))
        );
      }
    } catch (err: any) {
      console.error(`Failed to load messages for session ${sessionId}:`, err);
    } finally {
      setLoadingHistory(false);
      scrollToBottom();
    }
  };

  const activeConvo = conversations.find((c) => c.id === activeId);
  const messages = activeConvo?.messages || [];

  const scrollToBottom = () => {
    setTimeout(() => {
      if (threadRef.current) {
        threadRef.current.scrollIntoView({ behavior: 'smooth', block: 'end' });
      }
    }, 100);
  };

  const handleNewChat = async () => {
    setError(undefined);
    try {
      const res = await fetch('/api/sessions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: 'New conversation' }),
      });
      if (res.ok) {
        const data = await res.json();
        const serverSession = data.session;
        const newConvo: Conversation = {
          id: serverSession.id,
          title: serverSession.title || 'New conversation',
          messages: [],
          updatedAt: Date.now(),
          backendSessionId: serverSession.id,
        };
        setConversations((prev) => [newConvo, ...prev]);
        setActiveId(serverSession.id);
      } else {
        const fallbackId = Date.now().toString();
        const newConvo: Conversation = {
          id: fallbackId,
          title: 'New conversation',
          messages: [],
          updatedAt: Date.now(),
        };
        setConversations((prev) => [newConvo, ...prev]);
        setActiveId(fallbackId);
      }
    } catch (err) {
      const fallbackId = Date.now().toString();
      const newConvo: Conversation = {
        id: fallbackId,
        title: 'New conversation',
        messages: [],
        updatedAt: Date.now(),
      };
      setConversations((prev) => [newConvo, ...prev]);
      setActiveId(fallbackId);
    }
    if (window.innerWidth <= 860) setSidebarOpen(false);
  };

  const handleDelete = (id: string) => {
    setConversations((prev) => prev.filter((c) => c.id !== id));
    if (activeId === id) setActiveId(null);
  };

  const handleRename = (id: string, newTitle: string) => {
    setConversations((prev) =>
      prev.map((c) => (c.id === id ? { ...c, title: newTitle } : c))
    );
  };

  const handleSelectSession = (id: string) => {
    setActiveId(id);
    loadSessionMessages(id);
    if (window.innerWidth <= 860) setSidebarOpen(false);
  };

  const handleSend = async (text: string) => {
    let currentId = activeId;
    if (!currentId) {
      currentId = Date.now().toString();
      const newConvo: Conversation = {
        id: currentId,
        title: text.slice(0, 30) + (text.length > 30 ? '...' : ''),
        messages: [],
        updatedAt: Date.now(),
      };
      setConversations((prev) => [newConvo, ...prev]);
      setActiveId(currentId);
    }

    const newMessage: Message = { role: 'user', content: text };

    setConversations((prev) =>
      prev.map((c) => {
        if (c.id === currentId) {
          return { ...c, messages: [...c.messages, newMessage], updatedAt: Date.now() };
        }
        return c;
      })
    );

    setBusy(true);
    setError(undefined);
    scrollToBottom();

    const currentConvo = conversations.find((c) => c.id === currentId);
    const backendSessionId = currentConvo?.backendSessionId;

    const reqBody: Record<string, unknown> = { prompt: text };
    if (backendSessionId) {
      reqBody.session_id = backendSessionId;
    }

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(reqBody),
      });

      if (!res.ok) {
        let errJson: any = null;
        try {
          errJson = await res.json();
        } catch {}
        const msg =
          errJson?.error?.message ||
          `Backend server returned an error (HTTP ${res.status}).`;
        throw new Error(msg);
      }

      const data = await res.json();
      const botMessage: Message = {
        role: 'assistant',
        content: data.text || data.response || data.message || 'No response returned.',
      };

      setConversations((prev) =>
        prev.map((c) => {
          if (c.id === currentId) {
            return {
              ...c,
              backendSessionId: data.session_id || c.backendSessionId,
              title: c.title === 'New conversation' ? text.slice(0, 32) : c.title,
              messages: [...c.messages, botMessage],
              updatedAt: Date.now(),
            };
          }
          return c;
        })
      );
    } catch (err: any) {
      console.error('Chat execution failed:', err);
      setError(err?.message || 'Backend service connection failed. Please retry.');
    } finally {
      setBusy(false);
      scrollToBottom();
    }
  };

  const handleEdit = (index: number, newContent: string) => {
    if (!activeId) return;
    setConversations((prev) =>
      prev.map((c) => {
        if (c.id !== activeId) return c;
        const newMessages = c.messages.slice(0, index);
        return { ...c, messages: newMessages, updatedAt: Date.now() };
      })
    );
    handleSend(newContent);
  };

  const handleRegenerate = (index: number) => {
    if (!activeId || index === 0) return;
    const prevUserMsg = messages[index - 1];
    if (prevUserMsg?.role === 'user') {
      handleEdit(index - 1, prevUserMsg.content);
    }
  };

  return (
    <div className="chat-body">
      <div className="app">
        <Sidebar
          conversations={conversations}
          activeId={activeId}
          isOpen={sidebarOpen}
          onClose={() => setSidebarOpen(false)}
          onNewChat={handleNewChat}
          onSelect={handleSelectSession}
          onDelete={handleDelete}
          onRename={handleRename}
        />

        <main className="main">
          <header className="topbar">
            <button className="menu-btn" onClick={() => setSidebarOpen(true)}>
              <svg viewBox="0 0 24 24">
                <path
                  d="M3 12h18M3 6h18M3 18h18"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
            </button>
            <Link href="/" className="home">
              <svg viewBox="0 0 24 24">
                <path
                  d="M19 12H5M12 19l-7-7 7-7"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
              Home
            </Link>
            <div className="spacer" />
            <span className="mtag">Mind1.1 RTL Runtime</span>
          </header>

          <div className="scroll">
            <div className="thread">
              {messages.length === 0 ? (
                <div className="welcome">
                  <div className="wm">
                    <svg viewBox="0 0 32 32" fill="none">
                      <path
                        d="M16 4c-5 0-8 3-8 6.5 0 .8-2 1.5-2 4.5 0 2 1.4 3.4 1.4 5C7.4 22 10 24 13 24M16 4c5 0 8 3 8 6.5 0 .8 2 1.5 2 4.5 0 2-1.4 3.4-1.4 5C24.6 22 22 24 19 24M16 4v22"
                        stroke="#fff"
                        strokeWidth="2.2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      />
                    </svg>
                  </div>
                  <h1>How can I help with your RTL design?</h1>
                  <p>Generate synthesizable Verilog, write testbenches, or debug timing & simulation.</p>

                  <div className="suggests">
                    <div
                      className="sg"
                      onClick={() =>
                        handleSend(
                          'Write a synthesizable 8-bit arithmetic logic unit (ALU) in Verilog with zero, carry, and overflow flags.'
                        )
                      }
                    >
                      <b>Design an 8-bit ALU</b>
                      <span>Verilog, arithmetic + logic + flags</span>
                    </div>
                    <div
                      className="sg"
                      onClick={() =>
                        handleSend(
                          'Design a parameterized synchronous FIFO controller in SystemVerilog with full and empty flag generation.'
                        )
                      }
                    >
                      <b>Synchronous FIFO</b>
                      <span>SystemVerilog circular buffer</span>
                    </div>
                  </div>
                </div>
              ) : (
                messages.map((m, i) => (
                  <MessageTurn
                    key={i}
                    message={m}
                    index={i}
                    isLast={i === messages.length - 1}
                    onEdit={handleEdit}
                    onRegenerate={handleRegenerate}
                  />
                ))
              )}

              {busy && (
                <MessageTurn
                  message={{ role: 'assistant', content: '' }}
                  index={messages.length}
                  isLast={true}
                  isThinking={true}
                  onEdit={() => {}}
                  onRegenerate={() => {}}
                />
              )}

              {error && (
                <div
                  role="alert"
                  style={{
                    margin: '1.2rem auto',
                    maxWidth: '42rem',
                    padding: '0.9rem 1.2rem',
                    background: '#FEF2F2',
                    border: '1px solid #FCA5A5',
                    borderRadius: '10px',
                    color: '#991B1B',
                    fontSize: '0.92rem',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.75rem',
                    boxShadow: '0 2px 8px rgba(220, 38, 38, 0.08)',
                  }}
                >
                  <svg
                    width="20"
                    height="20"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="#DC2626"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    style={{ flexShrink: 0 }}
                  >
                    <circle cx="12" cy="12" r="10" />
                    <line x1="12" y1="8" x2="12" y2="12" />
                    <line x1="12" y1="16" x2="12.01" y2="16" />
                  </svg>
                  <div>
                    <strong>Connection Error:</strong> {error}
                  </div>
                </div>
              )}

              <div ref={threadRef} />
            </div>
          </div>

          <Composer onSend={handleSend} disabled={busy} />
        </main>
      </div>
    </div>
  );
}
