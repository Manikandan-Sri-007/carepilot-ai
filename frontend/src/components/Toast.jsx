function Toast({ message, type = "info", onClose }) {
    if (!message) {
        return null;
    }

    return (
        <div className={`toast ${type}`} role="status" aria-live="polite">
            <span>{message}</span>
            <button onClick={onClose}>×</button>
        </div>
    );
}

export default Toast;
