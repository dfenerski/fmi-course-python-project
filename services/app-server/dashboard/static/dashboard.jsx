const handleLogout = () => {
    document.querySelector('#default-logout-form').submit();
};

const getProp = propName => {
    return window.__DJANGO_STATE__[propName];
};

const TopBar = () => (
    <div
        style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            padding: '1rem 2rem',
            backgroundColor: '#0078D4',
            color: 'white',
        }}>
        <div style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>Welcome</div>
        <div>
            <fluent-button
                appearance='accent'
                style={{ display: 'none', marginRight: '0.5rem' }}>
                Profile
            </fluent-button>
            <fluent-button
                appearance='accent'
                style={{ display: 'none', marginRight: '0.5rem' }}>
                Settings
            </fluent-button>
            <fluent-button appearance='accent' onClick={handleLogout}>
                Logout
            </fluent-button>
        </div>
    </div>
);

const Card = ({ title, content }) => (
    <fluent-card
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
            title: `Symbols: ${getProp('my_symbols')}`,
            content: 'View your tracked symbols here.',
        },
        { title: 'Screener', content: 'Search and evaluate key market movers' },
        {
            title: 'Ask AI',
            content: (
                <fluent-button
                    appearance='accent'
                    onClick={() => {
                        alert(3);
                    }}>
                    Dig insights
                </fluent-button>
            ),
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
