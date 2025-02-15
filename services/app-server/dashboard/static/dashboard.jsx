const handleLogout = () => {
    document.querySelector('#default-logout-form').submit();
};

const getProp = propName => {
    return window.__DJANGO_STATE__[propName];
};

const TopBar = () => (
    <div
        style={{
            position: 'sticky',
            top: 0,
            zIndex: 1000, // ensure the bar is above other content
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            padding: '1rem 2rem',
            backgroundColor: '#0078D4',
            color: 'white',
        }}>
        <div style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>
            {getProp('tracker_name')}
        </div>
        <div>
            <fluent-button
                appearance='accent'
                style={{ marginRight: '0.5rem' }}>
                Stock Screener
            </fluent-button>
            <fluent-button appearance='accent' onClick={handleLogout}>
                Logout
            </fluent-button>
        </div>
    </div>
);

const Card = ({ title, content, isVisible }) => (
    <fluent-card
        {...(!isVisible ? { class: 'visibilityHidden' } : {})}
        style={{
            padding: '1rem',
            borderRadius: '8px',
            boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
            backgroundColor: 'white',
        }}>
        <h3 style={{ marginTop: 0 }}>{title}</h3>
        <p>{content}</p>
    </fluent-card>
);

const Dashboard = () => {
    const cards = [
        {
            isVisible: true,
            title: `Currently tracking ${getProp('tracker_symbol_count')} stocks`,
            content: (
                <>
                    <fluent-button
                        appearance='accent'
                        style={{ marginTop: '0.5rem' }}>
                        Manage
                    </fluent-button>
                </>
            ),
        },
        {
            isVisible: true,
            title: 'Tracker Settings',
            content: (
                <>
                    <fluent-button
                        appearance='accent'
                        style={{ marginTop: '0.5rem' }}>
                        Adjust tracker name
                    </fluent-button>
                    <br />
                    <fluent-button
                        appearance='accent'
                        style={{ marginTop: '0.5rem' }}>
                        Add another Stock
                    </fluent-button>
                </>
            ),
        },
        {
            title: '',
            content: '',
            isVisible: false,
        },
    ];

    return (
        <div style={{ backgroundColor: '#f3f3f3', minHeight: '100vh' }}>
            <TopBar />
            <div
                style={{
                    padding: '2rem',
                    display: 'grid',
                    gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
                    gap: '1.5rem',
                }}>
                {cards.map((card, index) => (
                    <Card
                        key={index}
                        title={card.title}
                        content={card.content}
                        isVisible={card.isVisible}
                        onPress='alert(1)'
                        onClick='alert(2)'>
                        test123
                    </Card>
                ))}
            </div>
        </div>
    );
};

ReactDOM.render(<Dashboard />, document.getElementById('react-root'));
