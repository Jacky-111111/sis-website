/* ============================================
   Global State
   ============================================ */
let currentIngredients = [];

// API endpoint configuration
// TODO: 修改为你的后端 API 地址
const API_BASE_URL = 'http://localhost:5000';  // Flask 默认端口
// const API_BASE_URL = 'http://localhost:8000';  // FastAPI 默认端口

/* ============================================
   Section Navigation
   ============================================ */
function showSection(sectionName) {
  // Hide all sections
  document.querySelectorAll('.section').forEach(section => {
    section.classList.remove('active');
  });

  // Show target section
  const targetSection = document.getElementById(`${sectionName}-section`);
  if (targetSection) {
    targetSection.classList.add('active');
  }

  // Scroll to top
  window.scrollTo(0, 0);
}

/* ============================================
   Tab Switching (Text/Photo)
   ============================================ */
function switchTab(tabName) {
  // Update tab buttons
  document.querySelectorAll('.tab').forEach(tab => {
    tab.classList.remove('active');
  });
  event.target.classList.add('active');

  // Update tab content
  document.querySelectorAll('.tab-content').forEach(content => {
    content.classList.remove('active');
  });
  document.getElementById(`${tabName}-tab`).classList.add('active');
}

/* ============================================
   Ingredient Parsing
   ============================================ */
function parseIngredients(text) {
  if (!text || !text.trim()) {
    return [];
  }

  // Split by comma, semicolon, or newline
  return text
    .split(/[,;\n]/)
    .map(item => item.trim())
    .filter(item => item.length > 0);
}

/* ============================================
   Mock AI Analysis Function (前端备用)
   如果后端 API 不可用，可以使用这个函数作为备用
   TODO: 接入 GNN 模型后，这个函数可以删除
   ============================================ */
function analyzeIngredientsMock(ingredients) {
  // Simulate API delay
  return new Promise((resolve) => {
    setTimeout(() => {
      // Convert to lowercase for matching
      const lowerIngredients = ingredients.map(ing => ing.toLowerCase());

      // Danger keywords
      const dangerKeywords = [
        'retinol',
        'aha',
        'bha',
        'salicylic',
        'benzoyl',
        'vitamin c',
        'niacinamide',
        'ascorbic acid',
        'glycolic acid',
        'lactic acid'
      ];

      // Check for danger keywords
      const foundDangerKeywords = lowerIngredients.filter(ing =>
        dangerKeywords.some(keyword => ing.includes(keyword))
      );

      // Determine status
      const hasMultipleDangerKeywords = foundDangerKeywords.length >= 2;
      const hasRetinolAndAcid =
        lowerIngredients.some(ing => ing.includes('retinol')) &&
        (lowerIngredients.some(ing => ing.includes('aha')) ||
         lowerIngredients.some(ing => ing.includes('bha')) ||
         lowerIngredients.some(ing => ing.includes('salicylic')) ||
         lowerIngredients.some(ing => ing.includes('glycolic')) ||
         lowerIngredients.some(ing => ing.includes('lactic')));
      const hasVitaminCAndNiacinamide =
        lowerIngredients.some(ing => ing.includes('vitamin c') || ing.includes('ascorbic')) &&
        lowerIngredients.some(ing => ing.includes('niacinamide'));

      const isDanger = hasMultipleDangerKeywords || hasRetinolAndAcid || hasVitaminCAndNiacinamide;

      // Calculate risk score
      let riskScore = 0;
      if (isDanger) {
        riskScore = Math.min(100, 40 + foundDangerKeywords.length * 15);
      } else {
        riskScore = Math.max(0, foundDangerKeywords.length * 5);
      }

      // Generate summary
      let summary = '';
      if (isDanger) {
        if (hasRetinolAndAcid) {
          summary = 'We detected a potential conflict: Retinol and acids (AHA/BHA) can cause excessive irritation and dryness when used together. Consider using them on alternate days or at different times (AM/PM).';
        } else if (hasVitaminCAndNiacinamide) {
          summary = 'We detected a potential conflict: Vitamin C and Niacinamide may cause flushing and reduce effectiveness when combined at high concentrations. Consider applying them at different times of day.';
        } else {
          summary = 'We detected multiple active ingredients that may cause irritation or reduce effectiveness when combined. Please review the suggestions and consider spacing out active ingredients across different days.';
        }
      } else {
        summary = 'Your ingredient combination appears to be safe! No significant conflicts were detected. You can proceed with confidence. Remember to patch test new products and use sunscreen daily, especially with active ingredients.';
      }

      resolve({
        status: isDanger ? 'danger' : 'safe',
        summary: summary,
        riskScore: riskScore
      });
    }, 600); // 600ms delay to simulate API call
  });
}

/* ============================================
   Real API Call to Backend
   TODO: 接入 GNN 模型后，确保后端 API 返回相同格式的数据
   ============================================ */
async function analyzeIngredients(ingredients) {
  try {
    // 尝试调用后端 API
    const response = await fetch(`${API_BASE_URL}/api/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ ingredients: ingredients })
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    const result = await response.json();
    return result;
  } catch (error) {
    console.warn('Backend API not available, using mock function:', error);
    // 如果后端不可用，使用 mock 函数
    return await analyzeIngredientsMock(ingredients);
  }
}

/* ============================================
   Handle Analyze Button Click
   ============================================ */
async function handleAnalyze() {
  // Get ingredients from textarea
  const input = document.getElementById('ingredients-input');
  const ingredientsText = input.value;

  // Parse ingredients
  const ingredients = parseIngredients(ingredientsText);

  if (ingredients.length === 0) {
    alert('Please enter at least one ingredient');
    return;
  }

  // Store ingredients
  currentIngredients = ingredients;

  // Show result section
  showSection('result');

  // Show loading state
  document.getElementById('loading-state').style.display = 'block';
  document.getElementById('result-card').style.display = 'none';
  document.getElementById('ingredients-display').style.display = 'none';

  // Display ingredients as chips
  const chipsContainer = document.getElementById('ingredient-chips');
  chipsContainer.innerHTML = '';
  ingredients.forEach(ingredient => {
    const chip = document.createElement('span');
    chip.className = 'ingredient-chip';
    chip.textContent = ingredient;
    chipsContainer.appendChild(chip);
  });

  // Show ingredients display
  document.getElementById('ingredients-display').style.display = 'block';

  // Analyze ingredients (调用后端 API 或使用 mock)
  const result = await analyzeIngredients(ingredients);

  // Hide loading state
  document.getElementById('loading-state').style.display = 'none';

  // Show result card
  const resultCard = document.getElementById('result-card');
  resultCard.style.display = 'block';
  resultCard.className = `result-card ${result.status}`;

  // Update result content
  document.getElementById('result-title').textContent = 
    result.status === 'safe' ? "It's Safe To Use!" : 'Danger';
  document.getElementById('risk-score-badge').textContent = 
    `Risk Score: ${result.riskScore}/100`;
  document.getElementById('result-summary-text').textContent = result.summary;
}


/* ============================================
   Initialize
   ============================================ */
// Ensure home section is shown on load
window.addEventListener('load', () => {
  showSection('home');
});
