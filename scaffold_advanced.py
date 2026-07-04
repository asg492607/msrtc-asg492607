import os

structure = {
    'ai-platform': {
        'html': ['ai-home.html', 'chat.html', 'history.html', 'settings.html', 'voice.html'],
        'css': ['ai.css'],
        'js': ['ai.js'],
        'data': ['responses.json']
    },
    'analytics': {
        'html': ['dashboard.html', 'reports.html', 'revenue.html', 'occupancy.html'],
        'css': ['analytics.css'],
        'js': ['analytics.js'],
        'data': ['analytics.json']
    },
    'workshop': {
        'html': ['dashboard.html', 'repairs.html', 'inventory.html', 'mechanics.html', 'certificates.html'],
        'css': ['workshop.css'],
        'js': ['workshop.js']
    },
    'vendor': {
        'html': ['dashboard.html', 'vendors.html', 'purchase-orders.html', 'contracts.html', 'invoices.html'],
        'css': ['vendor.css'],
        'js': ['vendor.js']
    },
    'presentation': {
        'html': ['launcher.html', 'demo.html', 'walkthrough.html', 'personas.html', 'architecture.html'],
        'css': ['presentation.css'],
        'js': ['presentation.js']
    }
}

for folder, contents in structure.items():
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    # create css dir
    css_dir = os.path.join(folder, 'css')
    if not os.path.exists(css_dir):
        os.makedirs(css_dir)
        
    for css_file in contents.get('css', []):
        open(os.path.join(css_dir, css_file), 'w').close()
        
    # create js dir
    js_dir = os.path.join(folder, 'js')
    if not os.path.exists(js_dir):
        os.makedirs(js_dir)
        
    for js_file in contents.get('js', []):
        open(os.path.join(js_dir, js_file), 'w').close()
        
    # create data dir if present
    if 'data' in contents:
        data_dir = os.path.join(folder, 'data')
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        for data_file in contents['data']:
            open(os.path.join(data_dir, data_file), 'w').close()
            
    # create html files
    for html_file in contents.get('html', []):
        open(os.path.join(folder, html_file), 'w').close()

print("File structure created successfully.")
