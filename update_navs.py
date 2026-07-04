import os

root_dir = r"C:\Users\Atharva\OneDrive\Desktop\msrtc"

# Subdirectories that should have the back button
portals = [
    'depot-portal',
    'hq-portal',
    'regional-portal',
    'driver-app',
    'conductor-app',
    'workshop',
    'vendor',
    'analytics',
    'command-center',
    'ai-platform',
    'workshop-portal',
    'vendor-portal'
]

for portal in portals:
    portal_path = os.path.join(root_dir, portal)
    if not os.path.exists(portal_path):
        continue
        
    for root, dirs, files in os.walk(portal_path):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Replace integration/launcher.html with admin.html
                content = content.replace('../integration/launcher.html', '../admin.html')
                content = content.replace('⬅️ Launcher', '⬅️ Admin Home')
                content = content.replace('⬅️ Back to Launcher', '⬅️ Admin Home')
                content = content.replace('Return to Central Launcher', 'Return to Admin Home')
                
                # If there is no admin.html link in the nav menu, we should inject it
                if '../admin.html' not in content and '<nav class="nav-menu">' in content:
                    # Inject at the end of the nav menu
                    nav_end_idx = content.find('</nav>')
                    if nav_end_idx != -1:
                        injection = '\n      <a href="../admin.html" class="nav-item" style="margin-top: auto; border-top: 1px solid rgba(255,255,255,0.1); border-radius: 0; padding-top: 15px;">⬅️ Admin Home</a>\n    '
                        content = content[:nav_end_idx] + injection + content[nav_end_idx:]
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)

print("Updated all portals to link back to admin.html")
