import { useState, useRef, useEffect } from 'react';
import { Conversation } from './types';
import { ConfirmDialog } from './ConfirmDialog';

interface ConversationListProps {
  conversations: Conversation[];
  activeId: string | null;
  onSelect: (id: string) => void;
  onDelete: (id: string) => void;
  onRename: (id: string, newTitle: string) => void;
}

export function ConversationList({
  conversations,
  activeId,
  onSelect,
  onDelete,
  onRename,
}: ConversationListProps) {
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editValue, setEditValue] = useState('');
  const [deleteId, setDeleteId] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (editingId && inputRef.current) {
      inputRef.current.focus();
      inputRef.current.select();
    }
  }, [editingId]);

  if (conversations.length === 0) {
    return (
      <div className="sb-list">
        <div className="sb-empty">
          No conversations yet.<br />
          Start a new chat to begin.
        </div>
      </div>
    );
  }

  const handleCommitRename = (id: string) => {
    if (editingId !== id) return;
    const val = editValue.trim();
    if (val) onRename(id, val);
    setEditingId(null);
  };

  const handleKeyDown = (e: React.KeyboardEvent, id: string) => {
    if (e.key === 'Enter') handleCommitRename(id);
    if (e.key === 'Escape') setEditingId(null);
  };

  return (
    <>
      <div className="sb-list">
        <div className="sb-label">Recents</div>
        {conversations.map((c) => {
          const isActive = c.id === activeId;
          const isEditing = c.id === editingId;

          return (
            <div
              key={c.id}
              className={`conv ${isActive ? 'active' : ''}`}
              onClick={() => {
                if (!isEditing) onSelect(c.id);
              }}
            >
              {isEditing ? (
                <input
                  ref={inputRef}
                  className="name-edit"
                  value={editValue}
                  onChange={(e) => setEditValue(e.target.value)}
                  onBlur={() => handleCommitRename(c.id)}
                  onKeyDown={(e) => handleKeyDown(e, c.id)}
                  onClick={(e) => e.stopPropagation()}
                />
              ) : (
                <span className="t" title={c.title}>
                  {c.title}
                </span>
              )}
              
              {!isEditing && (
                <span className="acts">
                  <button
                    className="ibtn"
                    title="Rename"
                    onClick={(e) => {
                      e.stopPropagation();
                      setEditValue(c.title);
                      setEditingId(c.id);
                    }}
                  >
                    <svg viewBox="0 0 24 24">
                      <path d="M12 20h9M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4z" />
                    </svg>
                  </button>
                  <button
                    className="ibtn danger"
                    title="Delete"
                    onClick={(e) => {
                      e.stopPropagation();
                      setDeleteId(c.id);
                    }}
                  >
                    <svg viewBox="0 0 24 24">
                      <path d="M3 6h18M8 6V4h8v2M19 6l-1 14H6L5 6" />
                    </svg>
                  </button>
                </span>
              )}
            </div>
          );
        })}
      </div>

      <ConfirmDialog
        open={deleteId !== null}
        onOpenChange={(open) => {
          if (!open) setDeleteId(null);
        }}
        onConfirm={() => {
          if (deleteId) onDelete(deleteId);
        }}
        title="Delete conversation?"
        description="This action cannot be undone."
      />
    </>
  );
}
