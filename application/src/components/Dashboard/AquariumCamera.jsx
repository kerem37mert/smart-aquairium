import { useEffect, useState } from "react";
import "./AquariumCamera.css";

const AquariumCamera = ({ cameraFrame }) => {
    const [isConnected, setIsConnected] = useState(false);

    useEffect(() => {
        // Kamera frame'i geliyorsa bağlı kabul et
        if (cameraFrame) {
            setIsConnected(true);
        }
    }, [cameraFrame]);

    return (
        <div className="aquarium-camera">
            <div className="camera-header">
                <h3>Canlı Kamera Görüntüsü</h3>
            </div>
            <div className="camera-view">
                {cameraFrame ? (
                    <img src={cameraFrame} alt="Akvaryum Görüntüsü" />
                ) : (
                    <div className="no-signal">
                        <div className="spinner"></div>
                        <p>Kamera bağlantısı bekleniyor...</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default AquariumCamera;
