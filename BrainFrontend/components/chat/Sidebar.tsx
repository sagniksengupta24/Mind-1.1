import Link from 'next/link';
import { ConversationList } from './ConversationList';
import { Conversation } from './types';

interface SidebarProps {
  conversations: Conversation[];
  activeId: string | null;
  isOpen: boolean;
  onClose: () => void;
  onNewChat: () => void;
  onSelect: (id: string) => void;
  onDelete: (id: string) => void;
  onRename: (id: string, newTitle: string) => void;
}

export function Sidebar({
  conversations,
  activeId,
  isOpen,
  onClose,
  onNewChat,
  onSelect,
  onDelete,
  onRename,
}: SidebarProps) {
  return (
    <>
      <aside className={`sidebar ${isOpen ? 'open' : ''}`}>
        <div className="sb-head">
          <Link href="/" className="sb-brand">
            <svg viewBox="0 0 32 32" fill="none">
              <path
                d="M16 4c-5 0-8 3-8 6.5 0 .8-2 1.5-2 4.5 0 2 1.4 3.4 1.4 5C7.4 22 10 24 13 24M16 4c5 0 8 3 8 6.5 0 .8 2 1.5 2 4.5 0 2-1.4 3.4-1.4 5C24.6 22 22 24 19 24M16 4v22M12 15c-2.6 0-4-1.2-4-3M20 15c2.6 0 4-1.2 4-3"
                stroke="#2B50E0"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
            Quoro<em>Mind</em>
          </Link>
        </div>
        <div className="sb-new">
          <button onClick={onNewChat}>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
              <path d="M12 5v14M5 12h14" />
            </svg>
            New chat
          </button>
        </div>
        <ConversationList
          conversations={conversations}
          activeId={activeId}
          onSelect={onSelect}
          onDelete={onDelete}
          onRename={onRename}
        />
      </aside>
      <div className={`scrim ${isOpen ? 'open' : ''}`} onClick={onClose} />
    </>
  );
}
