const DialogRole = Object.freeze({
    INFO: 'info',
    ERROR: 'error',
    SUCCESS: 'success',
});

class ModalDialog extends React.Component {
    componentDidMount() {
        if (this.dialog) {
            this.dialog.showModal();
        }
    }

    closeDialog = () => {
        if (this.dialog) {
            this.dialog.close();
        }
        const { container } = this.props;
        if (container) {
            ReactDOM.unmountComponentAtNode(container);
            container.remove();
        }
    };

    render() {
        const { content, buttons, role = DialogRole.INFO } = this.props;
        // https://experience.sap.com/fiori-design-android/wear-os-colors/
        const borderMap = {
            [DialogRole.ERROR]: '#FF5C77',
            [DialogRole.SUCCESS]: '#BDE986',
            [DialogRole.INFO]: 'rgba(0, 120, 212, 0.5)', // #0078D4
        };
        const boxShadowMap = {
            [DialogRole.ERROR]: '0 2px 10px #FF5C77',
            [DialogRole.SUCCESS]: '0 2px 10px #BDE986',
            [DialogRole.INFO]: '0 2px 10px rgba(0, 120, 212, 0.5)', // #0078D4
        };

        return (
            <dialog
                ref={el => (this.dialog = el)}
                style={{
                    borderRadius: '12px',
                    border: `2px solid ${borderMap[role]}`,
                    boxShadow: boxShadowMap[role],
                    padding: '1rem',
                }}>
                <div className='dialog-content'>{content}</div>
                <div
                    className='dialog-actions'
                    style={{ marginTop: '1rem', textAlign: 'right' }}>
                    {buttons.map((btn, idx) => (
                        <fluent-button
                            key={idx}
                            appearance={btn.appearance || 'accent'}
                            onClick={() => {
                                if (btn.onClick) btn.onClick();
                                this.closeDialog();
                            }}
                            style={{ marginLeft: '0.5rem' }}>
                            {btn.label}
                        </fluent-button>
                    ))}
                </div>
            </dialog>
        );
    }
}

class PopupManager {
    static showSubmittable(jsxContent) {
        const container = document.createElement('div');
        document.body.appendChild(container);

        const { promise, resolve, reject } = Promise.withResolvers();

        const buttons = [
            { label: 'OK', appearance: 'accent', onClick: resolve },
            { label: 'Cancel', appearance: 'subtle', onClick: reject },
        ];

        ReactDOM.createRoot(container).render(
            <ModalDialog
                content={jsxContent}
                buttons={buttons}
                container={container}
                role={DialogRole.INFO}
            />,
        );

        return promise;
    }

    static showError(textValue) {
        const container = document.createElement('div');
        document.body.appendChild(container);
        const content = (
            <div>
                <h3>Error</h3>
                <p>{textValue}</p>
            </div>
        );

        const { promise, resolve } = Promise.withResolvers();

        ReactDOM.createRoot(container).render(
            <ModalDialog
                content={content}
                buttons={[
                    { label: 'Close', appearance: 'accent', onClick: resolve },
                ]}
                container={container}
                role={DialogRole.ERROR}
            />,
        );

        return promise;
    }

    static showSuccess(textValue) {
        const container = document.createElement('div');
        document.body.appendChild(container);
        const content = (
            <div>
                <h3>Success</h3>
                <p>{textValue}</p>
            </div>
        );

        const { promise, resolve } = Promise.withResolvers();

        ReactDOM.createRoot(container).render(
            <ModalDialog
                content={content}
                buttons={[
                    { label: 'Close', appearance: 'accent', onClick: resolve },
                ]}
                container={container}
                role={DialogRole.SUCCESS}
            />,
        );

        return promise;
    }
}
