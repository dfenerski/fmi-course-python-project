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
            zIndex: 1000,
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
                Dashboard
            </fluent-button>
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

const SymbolList = ({ symbols, onDelete }) => {
    return (
        <div
            style={{
                display: 'flex',
                flexDirection: 'column',
                gap: '1rem',
                padding: '1rem',
            }}>
            {symbols.map(symbol => (
                <fluent-card key={symbol.id} style={{ padding: '1rem' }}>
                    <h2>
                        {symbol.symbol_name} ({symbol.symbol_symbol})
                    </h2>
                    <p>
                        <strong>Industry:</strong> {symbol.symbol_industry}
                    </p>
                    <p>
                        <strong>Sector:</strong> {symbol.symbol_sector}
                    </p>
                    {symbol.symbol_ir_website && (
                        <p>
                            <a
                                href={symbol.symbol_ir_website}
                                target='_blank'
                                rel='noopener noreferrer'>
                                Investor Website
                            </a>
                        </p>
                    )}
                    <p>
                        <small>Added to tracker on: {symbol.created_at}</small>
                    </p>
                    {symbol.is_favorite && (
                        <fluent-badge appearance='accent'>
                            Favorite
                        </fluent-badge>
                    )}
                    <div style={{ marginTop: '1rem' }}>
                        {false && (
                            <fluent-button
                                id={`summary-btn-${symbol.id}`}
                                appearance='accent'>
                                View Summary
                            </fluent-button>
                        )}
                        {false && (
                            <fluent-popover
                                anchor={`summary-btn-${symbol.id}`}
                                trigger='click'>
                                <div
                                    style={{
                                        padding: '1rem',
                                        maxWidth: '300px',
                                    }}>
                                    {symbol.symbol_businessSummary}
                                </div>
                            </fluent-popover>
                        )}
                        <fluent-button
                            appearance='accent'
                            style={{ marginLeft: '0.5rem' }}
                            onClick={() => onDelete(symbol.id)}>
                            Delete
                        </fluent-button>
                    </div>
                </fluent-card>
            ))}
        </div>
    );
};

const Dashboard = () => {
    const [symbols, setSymbols] = React.useState([]);

    React.useEffect(() => {
        const trackerSymbols = getProp('tracker_symbols') || [];
        setSymbols(trackerSymbols);
    }, []);

    const handleDelete = id => {
        setSymbols(symbols.filter(symbol => symbol.id !== id));
    };

    const handleAdd = () => {
        const newSymbol = {
            id: Date.now(),
            symbol_name: 'New Stock',
            symbol_symbol: 'NEW',
            symbol_industry: 'Industry',
            symbol_sector: 'Sector',
            symbol_businessSummary: 'This is a new stock added.',
            symbol_ir_website: '',
            created_at: new Date().toLocaleString(),
            modified_at: new Date().toLocaleString(),
            is_favorite: false,
        };
        setSymbols([...symbols, newSymbol]);

        NetworkManager.POST({
            hi: 123,
        });
    };

    return (
        <div>
            <TopBar />
            <SymbolList symbols={symbols} onDelete={handleDelete} />
            <div style={{ padding: '1rem', textAlign: 'center' }}>
                <fluent-button appearance='accent' onClick={handleAdd}>
                    Add Stock
                </fluent-button>
            </div>
        </div>
    );
};

ReactDOM.render(<Dashboard />, document.getElementById('react-root'));
