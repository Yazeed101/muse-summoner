/* Muse Summoner Admin Interface JavaScript */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Feather icons
    feather.replace();
    
    // Configuration page functionality
    if (document.getElementById('save-config')) {
        initConfigPage();
    }
    
    // Muse management page functionality
    if (document.getElementById('create-muse-btn')) {
        initMusePage();
    }
    
    // Muse detail page functionality
    if (document.getElementById('update-muse-btn')) {
        initMuseDetailPage();
    }
    
    // System status page functionality
    if (document.getElementById('system-status')) {
        initSystemPage();
    }
    
    // Documentation functionality
    initDocumentation();
});

function initConfigPage() {
    const saveConfigBtn = document.getElementById('save-config');
    const resetConfigBtn = document.getElementById('reset-config');
    const configSuccess = document.getElementById('config-success');
    const configError = document.getElementById('config-error');
    
    saveConfigBtn.addEventListener('click', function() {
        // Collect all configuration values
        const config = {};
        
        // General settings
        config.system_name = document.getElementById('system_name').value;
        config.debug_mode = document.getElementById('debug_mode').checked;
        config.default_muse = document.getElementById('default_muse').value;
        
        // Memory settings
        config.memory_enabled = document.getElementById('memory_enabled').checked;
        config.max_memory_entries = parseInt(document.getElementById('max_memory_entries').value);
        config.memory_relevance_threshold = parseFloat(document.getElementById('memory_relevance_threshold').value);
        config.memory_storage_dir = document.getElementById('memory_storage_dir').value;
        
        // Web application settings
        config.web_host = document.getElementById('web_host').value;
        config.web_port = parseInt(document.getElementById('web_port').value);
        config.session_timeout = parseInt(document.getElementById('session_timeout').value);
        
        // Customization settings
        config.allow_muse_creation = document.getElementById('allow_muse_creation').checked;
        config.allow_memory_clearing = document.getElementById('allow_memory_clearing').checked;
        config.allow_system_commands = document.getElementById('allow_system_commands').checked;
        
        // Response generation settings
        config.response_generation = {
            include_memory_references: document.getElementById('include_memory_references').checked,
            signature_question_probability: parseFloat(document.getElementById('signature_question_probability').value),
            max_response_length: parseInt(document.getElementById('max_response_length').value)
        };
        
        // Send to server
        fetch('/admin/config/update', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(config),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                configSuccess.style.display = 'block';
                configError.style.display = 'none';
                
                // Hide success message after 3 seconds
                setTimeout(function() {
                    configSuccess.style.display = 'none';
                }, 3000);
            } else {
                configError.style.display = 'block';
                configSuccess.style.display = 'none';
                configError.textContent = data.message;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            configError.style.display = 'block';
            configSuccess.style.display = 'none';
            configError.textContent = 'Error saving configuration: ' + error.message;
        });
    });
    
    resetConfigBtn.addEventListener('click', function() {
        if (confirm('Are you sure you want to reset all configuration to default values? This cannot be undone.')) {
            fetch('/admin/config/reset', {
                method: 'POST',
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Reload the page to show default values
                    window.location.reload();
                } else {
                    configError.style.display = 'block';
                    configSuccess.style.display = 'none';
                    configError.textContent = data.message;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                configError.style.display = 'block';
                configSuccess.style.display = 'none';
                configError.textContent = 'Error resetting configuration: ' + error.message;
            });
        }
    });
}

function initMusePage() {
    const createMuseBtn = document.getElementById('create-muse-btn');
    const submitMuseBtn = document.getElementById('submit-muse');
    const clearMemoryBtns = document.querySelectorAll('.clear-memory-btn');
    const museSuccess = document.getElementById('muse-success');
    const museError = document.getElementById('muse-error');
    
    // Initialize create muse modal
    const createMuseModal = new bootstrap.Modal(document.getElementById('createMuseModal'));
    
    createMuseBtn.addEventListener('click', function() {
        createMuseModal.show();
    });
    
    submitMuseBtn.addEventListener('click', function() {
        // Collect form data
        const museData = {
            name: document.getElementById('muse-name').value,
            trigger_phrase: document.getElementById('muse-trigger').value,
            voice_tone: document.getElementById('muse-voice').value,
            purpose: document.getElementById('muse-purpose').value,
            tasks_supported: document.getElementById('muse-tasks').value.split('\n').filter(task => task.trim() !== ''),
            catchphrases: document.getElementById('muse-catchphrases').value.split('\n').filter(phrase => phrase.trim() !== ''),
            signature_question: document.getElementById('muse-question').value,
            sample_tasks: document.getElementById('muse-samples').value.split('\n').filter(task => task.trim() !== ''),
            ritual_system: document.getElementById('muse-ritual').value || null
        };
        
        // TODO: Send to server to create muse
        // This would be implemented in a real system
        
        // For now, just show success and close modal
        createMuseModal.hide();
        museSuccess.style.display = 'block';
        museSuccess.textContent = `Muse "${museData.name}" created successfully!`;
        
        // Hide success message after 3 seconds
        setTimeout(function() {
            museSuccess.style.display = 'none';
        }, 3000);
    });
    
    // Clear memory buttons
    clearMemoryBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const museName = this.dataset.muse;
            
            if (confirm(`Are you sure you want to clear all memory for ${museName}? This cannot be undone.`)) {
                fetch(`/admin/muses/${encodeURIComponent(museName)}/clear_memory`, {
                    method: 'POST',
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        museSuccess.style.display = 'block';
                        museError.style.display = 'none';
                        museSuccess.textContent = data.message;
                        
                        // Hide success message after 3 seconds
                        setTimeout(function() {
                            museSuccess.style.display = 'none';
                        }, 3000);
                    } else {
                        museError.style.display = 'block';
                        museSuccess.style.display = 'none';
                        museError.textContent = data.message;
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    museError.style.display = 'block';
                    museSuccess.style.display = 'none';
                    museError.textContent = 'Error clearing memory: ' + error.message;
                });
            }
        });
    });
}

function initMuseDetailPage() {
    // This would be implemented for the muse detail page
    console.log('Muse detail page initialized');
}

function initSystemPage() {
    // This would be implemented for the system status page
    console.log('System status page initialized');
}

function initDocumentation() {
    // Documentation links
    const configDocs = document.getElementById('config-docs');
    const museDocs = document.getElementById('muse-docs');
    const apiDocs = document.getElementById('api-docs');
    
    if (configDocs) {
        configDocs.addEventListener('click', function(e) {
            e.preventDefault();
            // This would open configuration documentation
            alert('Configuration documentation would open here');
        });
    }
    
    if (museDocs) {
        museDocs.addEventListener('click', function(e) {
            e.preventDefault();
            // This would open muse creation documentation
            alert('Muse creation documentation would open here');
        });
    }
    
    if (apiDocs) {
        apiDocs.addEventListener('click', function(e) {
            e.preventDefault();
            // This would open API documentation
            alert('API documentation would open here');
        });
    }
}

// Export data functionality
document.addEventListener('click', function(e) {
    if (e.target && e.target.id === 'export-data') {
        fetch('/admin/export')
            .then(response => response.json())
            .then(data => {
                // Create a download link for the JSON data
                const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(data, null, 2));
                const downloadAnchorNode = document.createElement('a');
                downloadAnchorNode.setAttribute("href", dataStr);
                downloadAnchorNode.setAttribute("download", "muse_summoner_export.json");
                document.body.appendChild(downloadAnchorNode);
                downloadAnchorNode.click();
                downloadAnchorNode.remove();
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error exporting data: ' + error.message);
            });
    }
});
