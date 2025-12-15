import { useEffect, useRef, useState } from "react";
import "./App.css";
import Header from "./components/Header";
import Dashboard from "./components/Dashboard";
import DashBoardItem from "./components/Dashboard/DashboardItem";
import DashboardItemGroup from "./components/Dashboard/DashboardItemGroup";
import DashboardButton from "./components/Dashboard/DashboardButton";
import HistoryChart from "./components/Dashboard/HistoryChart";

const App = () => {
    const wsRef = useRef(null);

    const [fishCount, setFishCount] = useState(0);
    const [history, setHistory] = useState([]);
    const [water, setWater] = useState({
        ph: 0,
        ammonia: 0,
        nitrite: 0,
        nitrate: 0,
        temperature: 0,
        status: "-",
        color: "#000"
    });

    useEffect(() => {
        // WS BAĞLAN
        wsRef.current = new WebSocket("ws://136.114.212.51:5000/ws");

        wsRef.current.onopen = () => {
            console.log("WS bağlı");

            //Kendini web client olarak tanıt
            wsRef.current.send(JSON.stringify({
                client: "web"
            }));
        };

        wsRef.current.onmessage = (event) => {
            const data = JSON.parse(event.data);

            // Backend'ten gelen sensör güncellemesi
            if (data.type === "sensor_update") {
                const payload = data.payload;

                setFishCount(payload.fish_count);
                setWater(payload.water_quality);

                // Geçmiş veriyi güncelle
                setHistory(prev => {
                    const now = new Date();
                    const timeString = now.toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit', second: '2-digit' });

                    // Eğer son veri ile aynı saniyedeysek ekleme yapma (Throttle)
                    if (prev.length > 0 && prev[prev.length - 1].time === timeString) {
                        return prev;
                    }

                    const newData = {
                        time: timeString,
                        ph: payload.water_quality.ph,
                        ammonia: payload.water_quality.ammonia,
                        nitrite: payload.water_quality.nitrite,
                        nitrate: payload.water_quality.nitrate,
                        temperature: payload.water_quality.temperature
                    };

                    // Son 60 veriyi tut (Yaklaşık 1 dakika)
                    const newHistory = [...prev, newData];
                    if (newHistory.length > 60) {
                        return newHistory.slice(newHistory.length - 60);
                    }
                    return newHistory;
                });
            }
        };

        wsRef.current.onerror = (err) => {
            console.error("WS hata:", err);
        };

        wsRef.current.onclose = () => {
            console.log("WS kapandı");
        };

        return () => {
            wsRef.current?.close();
        };
    }, []);

    // =====================
    // BUTON AKSİYONLARI
    // =====================

    const sendCommand = (name) => {
        if (wsRef.current?.readyState === WebSocket.OPEN) {
            wsRef.current.send(JSON.stringify({
                type: "command",
                payload: { name }
            }));
        }
    };

    const feedBtnStyle = {
        backgroundColor: "rgb(60, 160, 80)",
        border: "2px solid rgb(40, 120, 60)",
    };

    const waterChangeBtn = {
        backgroundColor: "rgb(60, 130, 200)",
        border: "2px solid rgb(40, 100, 160)",
    };

    return (
        <>
            <Header title="Akıllı Akvaryum Yönetimi" />
            <Dashboard>
                <DashBoardItem label="Balık Sayısı" value={fishCount} />

                <DashboardItemGroup title="Su Kalitesi">
                    <DashBoardItem label="pH" value={water.ph.toFixed(1)} />
                    <DashBoardItem label="Sıcaklık" value={`${water.temperature.toFixed(1)} °C`} />
                    <DashBoardItem label="Amonyak" value={`${water.ammonia.toFixed(2)} ppm`} />
                    <DashBoardItem label="Nitrit" value={`${water.nitrite.toFixed(2)} ppm`} />
                    <DashBoardItem label="Nitrat" value={`${water.nitrate.toFixed(1)} ppm`} />
                    <DashBoardItem label="Durum" value={water.status} color={water.color} />
                </DashboardItemGroup>

                <div className="button-container">
                    <DashboardButton
                        text="Yem Ver"
                        style={feedBtnStyle}
                        onClick={() => sendCommand("feed")}
                    />
                    <DashboardButton
                        text="Suyu Değiştir"
                        style={waterChangeBtn}
                        onClick={() => sendCommand("water_change")}
                    />
                </div>

                <HistoryChart data={history} />
            </Dashboard>
        </>
    );
};

export default App;
