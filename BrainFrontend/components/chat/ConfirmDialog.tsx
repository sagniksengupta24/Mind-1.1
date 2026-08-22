'use client';

import * as Dialog from '@radix-ui/react-dialog';
import { motion, AnimatePresence } from 'framer-motion';

interface ConfirmDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onConfirm: () => void;
  title: string;
  description: string;
}

export function ConfirmDialog({ open, onOpenChange, onConfirm, title, description }: ConfirmDialogProps) {
  return (
    <Dialog.Root open={open} onOpenChange={onOpenChange}>
      <AnimatePresence>
        {open && (
          <Dialog.Portal forceMount>
            <Dialog.Overlay asChild>
              <motion.div
                className="overlay open"
                style={{ display: 'flex' }}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
              />
            </Dialog.Overlay>
            <Dialog.Content asChild>
              <motion.div
                className="modal"
                style={{
                  position: 'fixed',
                  top: '50%',
                  left: '50%',
                  transform: 'translate(-50%, -50%)',
                  zIndex: 100,
                }}
                initial={{ opacity: 0, scale: 0.95, x: '-50%', y: '-50%' }}
                animate={{ opacity: 1, scale: 1, x: '-50%', y: '-50%' }}
                exit={{ opacity: 0, scale: 0.95, x: '-50%', y: '-50%' }}
              >
                <Dialog.Title asChild>
                  <h3>{title}</h3>
                </Dialog.Title>
                <Dialog.Description asChild>
                  <p className="sub">{description}</p>
                </Dialog.Description>
                <div className="modal-actions" style={{ justifyContent: 'flex-end', marginTop: '1.5rem' }}>
                  <Dialog.Close asChild>
                    <button className="mini cancel">Cancel</button>
                  </Dialog.Close>
                  <button
                    className="mini save"
                    style={{ background: 'var(--cut)' }}
                    onClick={() => {
                      onConfirm();
                      onOpenChange(false);
                    }}
                  >
                    Delete
                  </button>
                </div>
              </motion.div>
            </Dialog.Content>
          </Dialog.Portal>
        )}
      </AnimatePresence>
    </Dialog.Root>
  );
}
