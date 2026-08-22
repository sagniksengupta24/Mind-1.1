import { useState, useRef, useEffect } from 'react';
import { Message } from './types';
import { ErrorBanner } from './ErrorBanner';

const BOT_SVG = (
  <svg viewBox="0 0 32 32" fill="none">
    <path
      d="M16 4c-5 0-8 3-8 6.5 0 .8-2 1.5-2 4.5 0 2 1.4 3.4 1.4 5C7.4 22 10 24 13 24M16 4c5 0 8 3 8 6.5 0 .8 2 1.5 2 4.5 0 2-1.4 3.4-1.4 5C24.6 22 22 24 19 24M16 4v22"
      stroke="#fff"
      strokeWidth="2.2"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </svg>
);

interface MessageTurnProps {
  message: Message;
  index: number;
  onEdit: (index: number, newContent: string) => void;
  onRegenerate: (index: number) => void;
  isLast: boolean;
  isThinking?: boolean;
  error?: string;
  onClearError?: () => void;
}

export function MessageTurn({
  message,
  index,
  onEdit,
  onRegenerate,
  isLast,
  isThinking,
  error,
  onClearError,
}: MessageTurnProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editValue, setEditValue] = useState(message.content);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (isEditing && textareaRef.current) {
      textareaRef.current.focus();
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = textareaRef.current.scrollHeight + 'px';
    }
  }, [isEditing]);

  const handleCopy = () => {
    if (navigator.clipboard) {
      navigator.clipboard.writeText(message.content);
    }
  };

  const handleSaveEdit = () => {
    const val = editValue.trim();
    if (val) {
      onEdit(index, val);
    }
    setIsEditing(false);
  };

  const isUser = message.role === 'user';

  return (
    <div className={`turn ${isUser ? 'user' : 'bot'}`}>
      {!isUser && (
        <div className="mark">
          {BOT_SVG}
        </div>
      )}
      
      <div className="col">
        {isEditing ? (
          <div className="edit-box">
            <textarea
              ref={textareaRef}
              value={editValue}
              onChange={(e) => setEditValue(e.target.value)}
            />
            <div className="edit-actions">
              <button className="mini cancel" onClick={() => setIsEditing(false)}>
                Cancel
              </button>
              <button className="mini save" onClick={handleSaveEdit}>
                Save &amp; submit
              </button>
            </div>
          </div>
        ) : (
          <>
            {isUser ? (
              <div className="user-bubble">{message.content}</div>
            ) : (
              <div className="prose">
                {message.content}
                {isThinking && (
                  <span className="thinking block mt-2">
                    Thinking<span className="d" />
                  </span>
                )}
                {error && (
                  <div className="mt-3">
                    <ErrorBanner message={error} onRetry={onClearError} />
                  </div>
                )}
              </div>
            )}
            
            <div className="tools" style={{ display: isEditing || error ? 'none' : '' }}>
              {isUser ? (
                <button className="ibtn" title="Edit" onClick={() => { setEditValue(message.content); setIsEditing(true); }}>
                  <svg viewBox="0 0 24 24">
                    <path d="M12 20h9M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4z" />
                  </svg>
                </button>
              ) : (
                <>
                  <button className="ibtn" title="Copy" onClick={handleCopy}>
                    <svg viewBox="0 0 24 24">
                      <rect x="9" y="9" width="13" height="13" rx="2" />
                      <path d="M5 15V5a2 2 0 0 1 2-2h10" />
                    </svg>
                  </button>
                  <button className="ibtn" title="Regenerate" onClick={() => onRegenerate(index)}>
                    <svg viewBox="0 0 24 24">
                      <path d="M23 4v6h-6M1 20v-6h6" />
                      <path d="M3.5 9a9 9 0 0 1 14.9-3.4L23 10M1 14l4.6 4.4A9 9 0 0 0 20.5 15" />
                    </svg>
                  </button>
                </>
              )}
            </div>
          </>
        )}
      </div>
    </div>
  );
}
