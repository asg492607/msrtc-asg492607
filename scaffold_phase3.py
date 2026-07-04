import os

structure = {
    'accessibility': {
        'html': ['accessibility.html', 'language-settings.html', 'keyboard-shortcuts.html'],
        'css': ['accessibility.css'],
        'js': ['accessibility.js'],
        'data': ['translations.json']
    },
    'tracking': {
        'html': ['live-tracking.html', 'bus-map.html', 'route-map.html', 'nearby-depots.html', 'nearby-stops.html'],
        'css': ['tracking.css'],
        'js': ['tracking.js'],
        'data': ['routes.json']
    },
    'careers': {
        'html': ['careers.html', 'openings.html', 'apply.html', 'application-status.html', 'employee-dashboard.html', 
                 'salary-slip.html', 'leave.html', 'attendance.html', 'transfer-request.html', 'training.html', 
                 'admit-card.html', 'results.html'],
        'css': ['employee.css'],
        'js': ['employee.js']
    },
    'governance': {
        'html': ['latest-news.html', 'circulars.html', 'tenders.html', 'acts-rules.html', 'citizen-charter.html', 
                 'achievements.html', 'awards.html', 'annual-reports.html', 'media-gallery.html', 'press-release.html'],
        'css': ['governance.css'],
        'js': ['governance.js']
    },
    'polish': {
        'html': ['demo-mode.html', 'onboarding.html', 'presentation.html'],
        'css': ['animations.css'],
        'js': ['motion.js'],
        'data': ['ui-audit.md']
    }
}

for folder, contents in structure.items():
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    # css dir
    css_dir = os.path.join(folder, 'css')
    if not os.path.exists(css_dir):
        os.makedirs(css_dir)
        
    for css_file in contents.get('css', []):
        open(os.path.join(css_dir, css_file), 'w').close()
        
    # js dir
    js_dir = os.path.join(folder, 'js')
    if not os.path.exists(js_dir):
        os.makedirs(js_dir)
        
    for js_file in contents.get('js', []):
        open(os.path.join(js_dir, js_file), 'w').close()
        
    # data/md files directly or in data folder
    for data_file in contents.get('data', []):
        if data_file.endswith('.json'):
            d_dir = os.path.join(folder, 'data')
            if not os.path.exists(d_dir):
                os.makedirs(d_dir)
            open(os.path.join(d_dir, data_file), 'w').close()
        else:
            open(os.path.join(folder, data_file), 'w').close()
            
    # html files
    for html_file in contents.get('html', []):
        open(os.path.join(folder, html_file), 'w').close()

print("Phase 3 structure created successfully.")
