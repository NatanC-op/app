```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Shelf & Stock Synchronizer - Phygital Retail SaaS</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        brand: {
                            50: '#f0f9ff',
                            100: '#e0f2fe',
                            500: '#0284c7',
                            600: '#0284c7',
                            700: '#0369a1',
                            900: '#0c4a6e',
                        }
                    }
                }
            }
        }
    </script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        body { font-family: 'Inter', sans-serif; }
        .scanner-laser {
            background: linear-gradient(180deg, rgba(239, 68, 68, 0) 0%, rgba(239, 68, 68, 0.8) 50%, rgba(239, 68, 68, 0) 100%);
            animation: scan 2s infinite ease-in-out;
        }
        @keyframes scan {
            0% { top: 0%; opacity: 0.3; }
            50% { top: 85%; opacity: 0.9; }
            100% { top: 0%; opacity: 0.3; }
        }
        .pulse-red {
            animation: pulse-red-anim 1.5s infinite;
        }
        @keyframes pulse-red-anim {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.8; transform: scale(1.02); }
        }
    </style>
</head>
<body class="bg-slate-900 text-slate-100 min-h-screen flex flex-col">

    <!-- Top Navigation Header -->
    <header class="bg-slate-800/80 backdrop-blur border-b border-slate-700 sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3 flex items-center justify-between">
            <div class="flex items-center space-x-3">
                <div class="bg-gradient-to-tr from-sky-500 to-indigo-600 p-2 rounded-xl text-white shadow-lg shadow-sky-500/20">
                    <i data-lucide="box" class="w-6 h-6"></i>
                </div>
                <div>
                    <h1 class="text-lg font-bold bg-gradient-to-r from-sky-400 to-indigo-300 bg-clip-text text-transparent">ShelfSync AI</h1>
                    <p class="text-xs text-slate-400 hidden sm:block">IoT Smart Shelf & Optical Stock Synchronizer</p>
                </div>
            </div>

            <!-- Quick Stats & Status -->
            <div class="flex items-center space-x-3">
                <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                    <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
                    IoT Gateway: Online
                </span>
                <button id="themeToggle" onclick="toggleSimulatedTheme()" class="p-2 rounded-lg bg-slate-700 hover:bg-slate-600 text-slate-300 transition-colors">
                    <i data-lucide="moon" class="w-4 h-4"></i>
                </button>
            </div>
        </div>
    </header>

    <!-- Main Container -->
    <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">

        <!-- Interactive Control Bar for Pitch / Demo -->
        <section class="bg-slate-800 border border-indigo-500/30 rounded-2xl p-4 shadow-xl">
            <div class="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
                <div>
                    <div class="flex items-center gap-2">
                        <span class="bg-indigo-500/20 text-indigo-300 text-xs font-semibold px-2.5 py-0.5 rounded-full border border-indigo-500/30">Investor Demo Control</span>
                        <h2 class="text-sm font-semibold text-slate-200">Simulate Real-World Scenarios</h2>
                    </div>
                    <p class="text-xs text-slate-400 mt-1">Test how the IoT load sensors and AI vision handle physical misplacements and automated reorders.</p>
                </div>
                
                <div class="flex flex-wrap items-center gap-2 w-full md:w-auto">
                    <button id="btnSimulateError" onclick="triggerMisplacementError()" class="flex-1 md:flex-none flex items-center justify-center gap-2 bg-rose-600 hover:bg-rose-500 text-white px-4 py-2 rounded-xl text-xs font-medium transition-all shadow-lg shadow-rose-600/20 active:scale-95">
                        <i data-lucide="alert-triangle" class="w-4 h-4"></i>
                        Simulate Human Error (Shelf B2)
                    </button>
                    <button id="btnCalibrate" onclick="triggerAICalibration()" class="flex-1 md:flex-none flex items-center justify-center gap-2 bg-sky-600 hover:bg-sky-500 text-white px-4 py-2 rounded-xl text-xs font-medium transition-all shadow-lg shadow-sky-600/20 active:scale-95">
                        <i data-lucide="scan" class="w-4 h-4"></i>
                        Trigger AI Camera Scan
                    </button>
                    <button id="btnResolve" onclick="resolveAllErrors()" class="flex-1 md:flex-none flex items-center justify-center gap-2 bg-emerald-600 hover:bg-emerald-500 text-white px-4 py-2 rounded-xl text-xs font-medium transition-all shadow-lg shadow-emerald-600/20 active:scale-95">
                        <i data-lucide="check-circle" class="w-4 h-4"></i>
                        Reset & Resolve
                    </button>
                </div>
            </div>
        </section>

        <!-- KPI Metrics Grid -->
        <section class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div class="bg-slate-800 border border-slate-700/60 rounded-2xl p-4">
                <div class="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
                    <span>Total Monitored Shelves</span>
                    <i data-lucide="layers" class="w-4 h-4 text-sky-400"></i>
                </div>
                <div class="text-2xl font-bold text-slate-100">12 Shelves</div>
                <div class="text-xs text-emerald-400 mt-1 flex items-center gap-1">
                    <i data-lucide="wifi" class="w-3 h-3"></i> 100% Signal Strength
                </div>
            </div>

            <div class="bg-slate-800 border border-slate-700/60 rounded-2xl p-4">
                <div class="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
                    <span>Active Stock Accuracy</span>
                    <i data-lucide="shield-check" class="w-4 h-4 text-emerald-400"></i>
                </div>
                <div id="kpiAccuracy" class="text-2xl font-bold text-emerald-400">99.4%</div>
                <div id="kpiAccuracySub" class="text-xs text-slate-400 mt-1">Real-time load verification</div>
            </div>

            <div class="bg-slate-800 border border-slate-700/60 rounded-2xl p-4">
                <div class="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
                    <span>Displacement Alerts</span>
                    <i data-lucide="alert-octagon" class="w-4 h-4 text-rose-400"></i>
                </div>
                <div id="kpiAlerts" class="text-2xl font-bold text-slate-100">0 Items</div>
                <div id="kpiAlertsSub" class="text-xs text-emerald-400 mt-1">Zero misplaced items</div>
            </div>

            <div class="bg-slate-800 border border-slate-700/60 rounded-2xl p-4">
                <div class="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
                    <span>Auto Supplier POs</span>
                    <i data-lucide="truck" class="w-3.5 h-3.5 text-indigo-400"></i>
                </div>
                <div id="kpiOrders" class="text-2xl font-bold text-slate-100">2 Pending</div>
                <div class="text-xs text-slate-400 mt-1">Synced with Global ERP</div>
            </div>
        </section>

        <!-- Main Dashboard Content Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">

            <!-- Left 7 Cols: Smart Shelf IoT Status & Camera Verification -->
            <div class="lg:col-span-7 space-y-6">

                <!-- Live Smart Shelf IoT Grid -->
                <div class="bg-slate-800 border border-slate-700/60 rounded-2xl p-5 shadow-sm">
                    <div class="flex items-center justify-between mb-4">
                        <div>
                            <h3 class="font-semibold text-slate-100 text-sm flex items-center gap-2">
                                <i data-lucide="cpu" class="w-4 h-4 text-sky-400"></i>
                                Live Smart Shelf Telemetry (IoT Load Sensors)
                            </h3>
                            <p class="text-xs text-slate-400">Sensors sample load weight every 500ms</p>
                        </div>
                        <span class="text-xs bg-slate-700 text-slate-300 px-2.5 py-1 rounded-md font-mono">HX711 Load Cells</span>
                    </div>

                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                        <!-- Shelf A1 -->
                        <div class="bg-slate-900/80 border border-slate-700 rounded-xl p-3.5 space-y-2">
                            <div class="flex justify-between items-center text-xs">
                                <span class="font-bold text-slate-200">Shelf A1</span>
                                <span class="bg-emerald-500/10 text-emerald-400 text-[10px] px-2 py-0.5 rounded-full font-medium border border-emerald-500/20">Normal</span>
                            </div>
                            <div class="text-xs text-slate-400">Product: <span class="text-slate-200 font-medium">Arabica Coffee (250g)</span></div>
                            <div class="bg-slate-800 p-2 rounded-lg font-mono text-xs space-y-1">
                                <div class="flex justify-between text-slate-400"><span>Target:</span> <span>3,750 g (15 pcs)</span></div>
                                <div class="flex justify-between text-emerald-400 font-bold"><span>Actual:</span> <span>3,750 g (15 pcs)</span></div>
                            </div>
                            <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                                <div class="bg-emerald-500 h-full" style="width: 100%"></div>
                            </div>
                        </div>

                        <!-- Shelf B2 (Target for Misplacement) -->
                        <div id="shelfB2Card" class="bg-slate-900/80 border border-slate-700 rounded-xl p-3.5 space-y-2 transition-all duration-300">
                            <div class="flex justify-between items-center text-xs">
                                <span class="font-bold text-slate-200">Shelf B2</span>
                                <span id="shelfB2Badge" class="bg-emerald-500/10 text-emerald-400 text-[10px] px-2 py-0.5 rounded-full font-medium border border-emerald-500/20">Normal</span>
                            </div>
                            <div class="text-xs text-slate-400">Product: <span class="text-slate-200 font-medium">Organic Chips (150g)</span></div>
                            <div class="bg-slate-800 p-2 rounded-lg font-mono text-xs space-y-1">
                                <div class="flex justify-between text-slate-400"><span>Target:</span> <span>1,500 g (10 pcs)</span></div>
                                <div id="shelfB2Weight" class="flex justify-between text-emerald-400 font-bold"><span>Actual:</span> <span>1,500 g (10 pcs)</span></div>
                            </div>
                            <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                                <div id="shelfB2Progress" class="bg-emerald-500 h-full transition-all duration-500" style="width: 100%"></div>
                            </div>
                        </div>

                        <!-- Shelf C3 -->
                        <div class="bg-slate-900/80 border border-slate-700 rounded-xl p-3.5 space-y-2">
                            <div class="flex justify-between items-center text-xs">
                                <span class="font-bold text-slate-200">Shelf C3</span>
                                <span class="bg-amber-500/10 text-amber-400 text-[10px] px-2 py-0.5 rounded-full font-medium border border-amber-500/20">Low Stock</span>
                            </div>
                            <div class="text-xs text-slate-400">Product: <span class="text-slate-200 font-medium">Mineral Water (600ml)</span></div>
                            <div class="bg-slate-800 p-2 rounded-lg font-mono text-xs space-y-1">
                                <div class="flex justify-between text-slate-400"><span>Target:</span> <span>6,000 g (10 pcs)</span></div>
                                <div class="flex justify-between text-amber-400 font-bold"><span>Actual:</span> <span>1,800 g (3 pcs)</span></div>
                            </div>
                            <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                                <div class="bg-amber-500 h-full" style="width: 30%"></div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- AI Camera Calibration & Visual Verification Viewport -->
                <div class="bg-slate-800 border border-slate-700/60 rounded-2xl p-5 shadow-sm space-y-4">
                    <div class="flex items-center justify-between">
                        <div>
                            <h3 class="font-semibold text-slate-100 text-sm flex items-center gap-2">
                                <i data-lucide="aperture" class="w-4 h-4 text-sky-400"></i>
                                AI Optical Vision Scanner (AR Viewfinder)
                            </h3>
                            <p class="text-xs text-slate-400">YOLOv8 Object Detection + OCR Expiry Verification</p>
                        </div>
                        <span id="aiScanStatus" class="text-xs font-medium px-2.5 py-1 rounded-md bg-slate-700 text-slate-300">Scanner Standby</span>
                    </div>

                    <!-- Simulated Camera Viewport -->
                    <div class="relative w-full h-64 sm:h-72 bg-slate-950 rounded-xl overflow-hidden border border-slate-700 flex items-center justify-center">
                        
                        <!-- Simulated Shelf Background Image -->
                        <div class="absolute inset-0 opacity-40 bg-[radial-gradient(#38bdf8_1px,transparent_1px)] [background-size:16px_16px]"></div>
                        
                        <!-- Shelf Graphic Mockup -->
                        <div class="relative z-10 w-full h-full p-6 flex flex-col justify-end space-y-4">
                            <!-- Simulated Shelf Items Row -->
                            <div class="flex items-end justify-center space-x-3 h-40">
                                <div class="w-12 h-28 bg-emerald-700/60 border-2 border-emerald-400/80 rounded-md flex flex-col justify-between p-1 text-[9px] text-center font-bold">
                                    <span>CHIPS</span>
                                    <span class="text-emerald-300">150g</span>
                                </div>
                                <div class="w-12 h-28 bg-emerald-700/60 border-2 border-emerald-400/80 rounded-md flex flex-col justify-between p-1 text-[9px] text-center font-bold">
                                    <span>CHIPS</span>
                                    <span class="text-emerald-300">150g</span>
                                </div>

                                <!-- Misplaced Item Container (Dynamically Toggled) -->
                                <div id="visualMisplacedItem" class="relative w-16 h-36 bg-slate-800 border-2 border-slate-600 rounded-md flex flex-col justify-between p-1 text-[9px] text-center font-bold transition-all duration-300 opacity-30">
                                    <span id="misplacedLabel" class="text-slate-400">EMPTY</span>
                                    <span id="misplacedSub" class="text-slate-500">-</span>
                                    
                                    <!-- Dynamic AI Bounding Box Overlay -->
                                    <div id="aiBoundingBox" class="hidden absolute -inset-2 border-2 border-rose-500 bg-rose-500/20 rounded-lg flex flex-col justify-between p-1">
                                        <span class="bg-rose-600 text-white text-[8px] font-bold px-1 rounded self-start">DISPLACED ITEM DETECTED</span>
                                        <span class="bg-slate-900/90 text-rose-300 text-[8px] font-mono p-0.5 rounded border border-rose-500/40">Water Bottle (+600g)<br>EXP: 12/2027</span>
                                    </div>
                                </div>

                                <div class="w-12 h-28 bg-emerald-700/60 border-2 border-emerald-400/80 rounded-md flex flex-col justify-between p-1 text-[9px] text-center font-bold">
                                    <span>CHIPS</span>
                                    <span class="text-emerald-300">150g</span>
                                </div>
                            </div>
                            <!-- Shelf Plank -->
                            <div class="w-full h-3 bg-slate-700 rounded-full border-t border-slate-500 shadow-md"></div>
                        </div>

                        <!-- Scanner Laser Overlay -->
                        <div id="scannerLaser" class="hidden absolute inset-x-0 h-8 scanner-laser pointer-events-none z-20"></div>

                        <!-- Camera Grid Lines -->
                        <div class="absolute inset-0 border border-sky-500/20 pointer-events-none grid grid-cols-3 grid-rows-3">
                            <div class="border-r border-b border-sky-500/10"></div>
                            <div class="border-r border-b border-sky-500/10"></div>
                            <div class="border-b border-sky-500/10"></div>
                            <div class="border-r border-b border-sky-500/10"></div>
                            <div class="border-r border-b border-sky-500/10"></div>
                            <div class="border-b border-sky-500/10"></div>
                        </div>
                    </div>

                    <!-- Scan Results Summary Bar -->
                    <div id="scanResultsSummary" class="bg-slate-900/90 border border-slate-700 rounded-xl p-3 flex flex-col sm:flex-row items-center justify-between text-xs gap-2">
                        <div class="flex items-center gap-2 text-slate-300">
                            <i data-lucide="info" class="w-4 h-4 text-sky-400"></i>
                            <span>Optical AI verifies item identity & matches against weight delta.</span>
                        </div>
                        <span id="scanResultBadge" class="bg-slate-800 text-slate-400 px-3 py-1 rounded-md font-mono">Status: Idle</span>
                    </div>
                </div>

            </div>

            <!-- Right 5 Cols: Logs, Supplier PO, ESG Metrics -->
            <div class="lg:col-span-5 space-y-6">

                <!-- Real-time Anomaly & Prevention Logs -->
                <div class="bg-slate-800 border border-slate-700/60 rounded-2xl p-5 shadow-sm space-y-3">
                    <div class="flex items-center justify-between">
                        <h3 class="font-semibold text-slate-100 text-sm flex items-center gap-2">
                            <i data-lucide="list-filter" class="w-4 h-4 text-indigo-400"></i>
                            Real-time Event Audit Stream
                        </h3>
                        <span class="text-[10px] text-slate-400 font-mono">Live WebSocket</span>
                    </div>

                    <div id="eventLogStream" class="space-y-2 max-h-48 overflow-y-auto pr-1 font-mono text-xs">
                        <div class="bg-slate-900/60 border border-slate-700/50 rounded-lg p-2.5 text-slate-300 flex items-start gap-2">
                            <span class="text-slate-500 text-[10px]">10:14:02</span>
                            <div>
                                <p class="text-emerald-400 font-medium">[SYSTEM READY] IoT Gateway synchronized.</p>
                                <p class="text-[11px] text-slate-400">12 Load cells responding normal.</p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Supplier Automation & Reorder Stream -->
                <div class="bg-slate-800 border border-slate-700/60 rounded-2xl p-5 shadow-sm space-y-3">
                    <div class="flex items-center justify-between">
                        <h3 class="font-semibold text-slate-100 text-sm flex items-center gap-2">
                            <i data-lucide="shopping-cart" class="w-4 h-4 text-amber-400"></i>
                            Automated Supplier Reorders
                        </h3>
                        <span class="text-[10px] bg-amber-500/10 text-amber-400 border border-amber-500/20 px-2 py-0.5 rounded">Auto-Pilot</span>
                    </div>

                    <div id="supplierOrdersList" class="space-y-2 text-xs">
                        <!-- Order item -->
                        <div class="bg-slate-900/60 border border-slate-700/50 rounded-lg p-3 flex items-center justify-between">
                            <div>
                                <div class="font-medium text-slate-200">Mineral Water 600ml</div>
                                <div class="text-[11px] text-slate-400">Supplier: AquaDistro Ltd. (Auto PO #9482)</div>
                            </div>
                            <span class="bg-amber-500/10 text-amber-400 border border-amber-500/20 px-2 py-1 rounded text-[10px] font-medium">Triggered (Low Stock)</span>
                        </div>
                    </div>
                </div>

                <!-- Carbon & Efficiency ESG Metrics -->
                <div class="bg-gradient-to-br from-slate-800 to-slate-800/80 border border-emerald-500/20 rounded-2xl p-5 shadow-sm space-y-3">
                    <div class="flex items-center justify-between">
                        <h3 class="font-semibold text-emerald-400 text-sm flex items-center gap-2">
                            <i data-lucide="leaf" class="w-4 h-4 text-emerald-400"></i>
                            Sustainability & Cost Impact
                        </h3>
                        <span class="text-[10px] bg-emerald-500/10 text-emerald-300 border border-emerald-500/30 px-2 py-0.5 rounded">ESG Verified</span>
                    </div>

                    <div class="grid grid-cols-2 gap-3 text-xs">
                        <div class="bg-slate-900/60 p-3 rounded-xl border border-slate-700/50">
                            <div class="text-slate-400 text-[11px]">Food Waste Reduced</div>
                            <div class="text-lg font-bold text-emerald-400 mt-0.5">-34%</div>
                            <div class="text-[10px] text-slate-500">Via OCR Expiry Alerts</div>
                        </div>

                        <div class="bg-slate-900/60 p-3 rounded-xl border border-slate-700/50">
                            <div class="text-slate-400 text-[11px]">Staff Audit Hours Saved</div>
                            <div class="text-lg font-bold text-sky-400 mt-0.5">18 hrs/wk</div>
                            <div class="text-[10px] text-slate-500">Automated stock counts</div>
                        </div>
                    </div>
                </div>

            </div>

        </div>

    </main>

    <!-- Footer with Business Plan Credits -->
    <footer class="bg-slate-800/60 border-t border-slate-700/60 py-4 mt-auto">
        <div class="max-w-7xl mx-auto px-4 text-center text-xs text-slate-400 flex flex-col sm:flex-row items-center justify-between gap-2">
            <div>
                <span class="font-semibold text-slate-200">ShelfSync AI</span> &mdash; SMA Business Plan Phygital Concept
            </div>
            <div class="flex items-center space-x-4 text-slate-500">
                <span>IoT Load Cells + AI Computer Vision</span>
                <span>&bull;</span>
                <span>Go-International SaaS Model</span>
            </div>
        </div>
    </footer>

    <!-- Interactive JavaScript Logic -->
    <script>
        // Initialize Lucide Icons
        lucide.createIcons();

        // State Management
        const state = {
            hasError: false,
            isScanning: false,
            shelfB2Weight: 1500, // Normal: 10 chips * 150g = 1500g
            targetWeight: 1500,
        };

        // DOM Elements
        const shelfB2Card = document.getElementById('shelfB2Card');
        const shelfB2Badge = document.getElementById('shelfB2Badge');
        const shelfB2Weight = document.getElementById('shelfB2Weight');
        const shelfB2Progress = document.getElementById('shelfB2Progress');
        const visualMisplacedItem = document.getElementById('visualMisplacedItem');
        const misplacedLabel = document.getElementById('misplacedLabel');
        const misplacedSub = document.getElementById('misplacedSub');
        const aiBoundingBox = document.getElementById('aiBoundingBox');
        const scannerLaser = document.getElementById('scannerLaser');
        const aiScanStatus = document.getElementById('aiScanStatus');
        const scanResultsSummary = document.getElementById('scanResultsSummary');
        const scanResultBadge = document.getElementById('scanResultBadge');
        const eventLogStream = document.getElementById('eventLogStream');
        
        const kpiAccuracy = document.getElementById('kpiAccuracy');
        const kpiAccuracySub = document.getElementById('kpiAccuracySub');
        const kpiAlerts = document.getElementById('kpiAlerts');
        const kpiAlertsSub = document.getElementById('kpiAlertsSub');

        // Helper Log Stream Generator
        function logEvent(title, detail, type = 'info') {
            const timeStr = new Date().toLocaleTimeString('en-US', { hour12: false });
            const logEntry = document.createElement('div');
            
            let colorClass = 'text-sky-400';
            if (type === 'error') colorClass = 'text-rose-400';
            if (type === 'success') colorClass = 'text-emerald-400';
            if (type === 'warning') colorClass = 'text-amber-400';

            logEntry.className = 'bg-slate-900/60 border border-slate-700/50 rounded-lg p-2.5 text-slate-300 flex items-start gap-2 animate-fadeIn';
            logEntry.innerHTML = `
                <span class="text-slate-500 text-[10px]">${timeStr}</span>
                <div>
                    <p class="${colorClass} font-medium">${title}</p>
                    <p class="text-[11px] text-slate-400">${detail}</p>
                </div>
            `;
            eventLogStream.prepend(logEntry);
        }

        // Trigger Scenario 1: Misplacement Error
        function triggerMisplacementError() {
            if (state.hasError) return;
            state.hasError = true;

            // Update Shelf B2 IoT Card UI
            shelfB2Card.className = 'bg-slate-900/80 border-2 border-rose-500/80 rounded-xl p-3.5 space-y-2 pulse-red shadow-lg shadow-rose-500/10';
            shelfB2Badge.className = 'bg-rose-500/20 text-rose-300 text-[10px] px-2 py-0.5 rounded-full font-bold border border-rose-500/40';
            shelfB2Badge.innerText = 'LOAD ANOMALY';

            shelfB2Weight.innerHTML = `<span>Actual:</span> <span class="text-rose-400">2,100 g (+600g Delta)</span>`;
            shelfB2Progress.className = 'bg-rose-500 h-full transition-all duration-500';
            shelfB2Progress.style.width = '100%';

            // Visual viewport change
            visualMisplacedItem.className = 'relative w-16 h-36 bg-cyan-900/80 border-2 border-cyan-400 rounded-md flex flex-col justify-between p-1 text-[9px] text-center font-bold transition-all duration-300 shadow-lg';
            misplacedLabel.className = 'text-cyan-200';
            misplacedLabel.innerText = 'WATER BOTTLE';
            misplacedSub.className = 'text-cyan-300';
            misplacedSub.innerText = '600g';

            // KPI Changes
            kpiAccuracy.innerText = '91.2%';
            kpiAccuracy.className = 'text-2xl font-bold text-rose-400';
            kpiAccuracySub.innerText = 'Anomali Delta at Shelf B2';

            kpiAlerts.innerText = '1 Item';
            kpiAlerts.className = 'text-2xl font-bold text-rose-400';
            kpiAlertsSub.innerText = 'Product Displacement Error';

            logEvent('[ANOMALY ALERT] Load Sensor Delta at Shelf B2', 'Unexpected +600g detected. Weight signature does not match Organic Chips.', 'error');
        }

        // Trigger Scenario 2: AI Optical Camera Verification
        function triggerAICalibration() {
            if (state.isScanning) return;
            state.isScanning = true;

            scannerLaser.classList.remove('hidden');
            aiScanStatus.className = 'text-xs font-medium px-2.5 py-1 rounded-md bg-sky-500/20 text-sky-300 border border-sky-500/30 animate-pulse';
            aiScanStatus.innerText = 'AI Scanning Camera Active...';

            logEvent('[AI VISION] Camera viewport activated', 'Processing YOLOv8 object detection on Shelf B2...', 'warning');

            setTimeout(() => {
                scannerLaser.classList.add('hidden');
                state.isScanning = false;

                if (state.hasError) {
                    aiBoundingBox.classList.remove('hidden');
                    aiScanStatus.className = 'text-xs font-medium px-2.5 py-1 rounded-md bg-rose-500/20 text-rose-300 border border-rose-500/30';
                    aiScanStatus.innerText = 'Displacement Verified';

                    scanResultBadge.className = 'bg-rose-500/20 text-rose-300 border border-rose-500/30 px-3 py-1 rounded-md font-mono font-bold';
                    scanResultBadge.innerText = 'Mismatch Detected: Water Bottle on Chips Shelf';

                    logEvent('[AI VERIFICATION COMPLETE]', 'Identified "Mineral Water 600ml" placed on "Organic Chips" shelf. OCR Expiry: 12/2027.', 'error');
                } else {
                    aiScanStatus.className = 'text-xs font-medium px-2.5 py-1 rounded-md bg-emerald-500/20 text-emerald-300 border border-emerald-500/30';
                    aiScanStatus.innerText = 'Calibration Normal';

                    scanResultBadge.className = 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 px-3 py-1 rounded-md font-mono';
                    scanResultBadge.innerText = 'Status: All Items Correctly Placed';

                    logEvent('[AI VERIFICATION COMPLETE]', 'Optical count matches load cell weights. Zero anomalies.', 'success');
                }
            }, 2000);
        }

        // Resolve / Reset Scenario
        function resolveAllErrors() {
            state.hasError = false;
            state.isScanning = false;

            // Reset UI
            shelfB2Card.className = 'bg-slate-900/80 border border-slate-700 rounded-xl p-3.5 space-y-2 transition-all duration-300';
            shelfB2Badge.className = 'bg-emerald-500/10 text-emerald-400 text-[10px] px-2 py-0.5 rounded-full font-medium border border-emerald-500/20';
            shelfB2Badge.innerText = 'Normal';

            shelfB2Weight.innerHTML = `<span>Actual:</span> <span>1,500 g (10 pcs)</span>`;
            shelfB2Weight.className = 'flex justify-between text-emerald-400 font-bold';
            shelfB2Progress.className = 'bg-emerald-500 h-full transition-all duration-500';

            visualMisplacedItem.className = 'relative w-16 h-36 bg-slate-800 border-2 border-slate-600 rounded-md flex flex-col justify-between p-1 text-[9px] text-center font-bold transition-all duration-300 opacity-30';
            misplacedLabel.className = 'text-slate-400';
            misplacedLabel.innerText = 'EMPTY';
            misplacedSub.className = 'text-slate-500';
            misplacedSub.innerText = '-';

            aiBoundingBox.classList.add('hidden');
            scannerLaser.classList.add('hidden');

            aiScanStatus.className = 'text-xs font-medium px-2.5 py-1 rounded-md bg-slate-700 text-slate-300';
            aiScanStatus.innerText = 'Scanner Standby';

            scanResultBadge.className = 'bg-slate-800 text-slate-400 px-3 py-1 rounded-md font-mono';
            scanResultBadge.innerText = 'Status: Idle';

            // KPI Changes
            kpiAccuracy.innerText = '99.4%';
            kpiAccuracy.className = 'text-2xl font-bold text-emerald-400';
            kpiAccuracySub.innerText = 'Real-time load verification';

            kpiAlerts.innerText = '0 Items';
            kpiAlerts.className = 'text-2xl font-bold text-slate-100';
            kpiAlertsSub.innerText = 'Zero misplaced items';

            logEvent('[RESOLVED]', 'Displaced item returned to correct shelf. System synchronized.', 'success');
        }

        // Dark/Light Theme Switcher Placeholder
        function toggleSimulatedTheme() {
            document.body.classList.toggle('bg-slate-900');
            document.body.classList.toggle('bg-slate-950');
        }
    </script>
</body>
</html>
```