# UPGRADE PLAN

## Issues Identified & Fixes

### 1. 🐛 Bug Fixes (Engine)
- Indentation bug in `engine.py` reset() method (lines 147-150)
- Missing terminal state handling in `_check_mission_completion()`
- Unreachable target check incomplete

### 2. ⚡ Performance Optimization
- Cache pathfinding results in `select_target()` 
- Optimize heatmap recalculation
- Reduce deep copy overhead
- Add path caching mechanism

### 3. 🧠 Architecture Improvements
- Extract common pathfinding boilerplate
- Better state machine for engine lifecycle
- Consistent error handling

### 4. 🎨 UI Enhancements
- Optimize renderer with dirty flags
- Better visual feedback
- Improved sidebar layout

### 5. 🏗️ Map Generator Improvements  
- Better room placement algorithm
- More varied entity distribution

### 6. 📝 Code Quality
- Comprehensive type hints
- Fix linting issues
- Remove unused imports
- Better docstrings