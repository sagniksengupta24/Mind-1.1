import { useState, useRef, useEffect } from 'react';

interface ComposerProps {
  onSend: (text: string) => void;
  disabled: boolean;
}

export function Composer({ onSend, disabled }: ComposerProps) {
  const [value, setValue] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = () => {
    const text = value.trim();
    if (!text || disabled) return;
    onSend(text);
    setValue('');
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setValue(e.target.value);
  };

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 200) + 'px';
    }
  }, [value]);

  return (
    <div className="composer-wrap">
      <div className="composer">
        <div className="composer-row">
          <textarea
            ref={textareaRef}
            rows={1}
            placeholder="Message QuoroMind…"
            value={value}
            onChange={handleChange}
            onKeyDown={handleKeyDown}
            disabled={disabled}
          />
          <button
            className="send"
            aria-label="Send"
            onClick={handleSubmit}
            disabled={disabled || !value.trim()}
          >
            <svg viewBox="0 0 24 24">
              <path d="M12 19V5M5 12l7-7 7 7" />
            </svg>
          </button>
        </div>
      </div>
      <p className="composer-hint">
        QuoroMind can make mistakes. Conversations are saved in this browser.
      </p>
    </div>
  );
}
