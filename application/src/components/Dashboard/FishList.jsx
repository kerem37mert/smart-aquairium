import "./FishList.css";

const FishList = ({ fishes }) => {
    if (!fishes || fishes.length === 0) {
        return (
            <div className="fish-list-container">
                <h3 className="fish-list-title">🐠 Balıklar</h3>
                <p className="no-fish-message">Henüz balık yok</p>
            </div>
        );
    }

    return (
        <div className="fish-list-container">
            <h3 className="fish-list-title">🐠 Balıklar ({fishes.length})</h3>
            <div className="fish-cards">
                {fishes.map((fish) => (
                    <div key={fish.id} className="fish-card">
                        <div className="fish-card-header">
                            <div className="fish-color-indicator" style={{ backgroundColor: fish.color }}></div>
                            <span className="fish-species">{fish.species}</span>
                        </div>
                        <div className="fish-details">
                            <div className="fish-detail-row">
                                <span className="detail-label">Yaş:</span>
                                <span className="detail-value">{fish.age} ay</span>
                            </div>
                            <div className="fish-detail-row">
                                <span className="detail-label">Cinsiyet:</span>
                                <span className="detail-value">{fish.gender === "Erkek" ? "♂️ Erkek" : "♀️ Dişi"}</span>
                            </div>
                            <div className="fish-detail-row">
                                <span className="detail-label">Boyut:</span>
                                <span className="detail-value">{fish.size} px</span>
                            </div>
                            <div className="fish-detail-row">
                                <span className="detail-label">Sağlık:</span>
                                <span className={`detail-value health-${fish.health === "Sağlıklı" ? "good" : "watch"}`}>
                                    {fish.health === "Sağlıklı" ? "✓ " : "⚠ "}{fish.health}
                                </span>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default FishList;
