# Testing with Dependency Injection

## Why DI Makes Testing Easier

Type-based dependency injection enables testing by allowing you to replace real dependencies with mocks or test doubles. The clear type signatures make it obvious what needs to be mocked.

---

## Testing Problems with Old Pattern

### Before Type-based DI

```python
class DatasetCollectionManager:

     def __init__(self, app: StructuredApp):
        self.model = app.model
        self.security = app.security
        self.hda_manager = hdas.HDAManager(app)
        self.history_manager = histories.HistoryManager(app)
        # ... more dependencies
```

**Testing Challenges:**
- What parts of `app` are being used?
- How do we construct a smaller app with just those pieces?
- How do we stub out classes cleanly when we're creating the dependent objects internally?

---

## Testing Benefits with Type-based DI

### After Type-based DI

```python
class DatasetCollectionManager:
    def __init__(
        self,
        model: GalaxyModelMapping,
        security: IdEncodingHelper,
        hda_manager: HDAManager,
        history_manager: HistoryManager,
        tag_handler: GalaxyTagHandler,
        ldda_manager: LDDAManager,
    ):
        self.model = model
        self.security = security
        self.hda_manager = hda_manager
        self.history_manager = history_manager
        self.tag_handler = tag_handler
        self.ldda_manager = ldda_manager
```

**Testing Benefits:**
- Type signature clearly shows all dependencies
- Can inject precise mocks for each dependency
- No need to construct entire `app` object
- Easy to test with minimal setup

---

## Unit Testing Example

### Mocking Dependencies

```python
from unittest.mock import Mock
import pytest
from galaxy.managers.collections import DatasetCollectionManager

def test_dataset_collection_manager():
    """Test with mocked dependencies."""
    # Create mocks for each dependency
    mock_model = Mock()
    mock_security = Mock()
    mock_hda_manager = Mock()
    mock_history_manager = Mock()
    mock_tag_handler = Mock()
    mock_ldda_manager = Mock()
    
    # Create manager with mocked dependencies
    manager = DatasetCollectionManager(
        model=mock_model,
        security=mock_security,
        hda_manager=mock_hda_manager,
        history_manager=mock_history_manager,
        tag_handler=mock_tag_handler,
        ldda_manager=mock_ldda_manager,
    )
    
    # Test the manager
    result = manager.some_method()
    
    # Verify interactions
    mock_hda_manager.some_method.assert_called_once()
```

---

## Testing Controllers

### FastAPI Controller Testing

```python
from unittest.mock import Mock
from galaxy.webapps.galaxy.api.tags import FastAPITags

def test_fastapi_tags_controller():
    """Test FastAPI controller with DI."""
    # Mock the manager
    mock_manager = Mock()
    mock_manager.update.return_value = {"status": "ok"}
    
    # Create controller with mocked manager
    controller = FastAPITags()
    controller.manager = mock_manager
    
    # Test
    trans = Mock()
    payload = Mock()
    result = controller.update(trans, payload)
    
    # Verify
    mock_manager.update.assert_called_once_with(trans, payload)
```

---

## Testing Legacy WSGI Controllers

### WSGI Controller Testing

```python
def test_legacy_tags_controller():
    """Test legacy WSGI controller with DI."""
    mock_manager = Mock()
    
    controller = TagsController()
    controller.manager = mock_manager
    
    # Test controller methods
    result = controller.index(trans)
    
    # Verify manager was used correctly
    mock_manager.list.assert_called_once()
```

---

## Testing Celery Tasks

### Task Testing

```python
from unittest.mock import Mock, patch
from galaxy.celery.tasks import purge_hda

def test_purge_hda_task():
    """Test Celery task with DI."""
    # Mock the manager
    mock_hda_manager = Mock()
    mock_hda = Mock()
    mock_hda_manager.by_id.return_value = mock_hda
    
    # Call task directly with mocked dependency
    purge_hda(hda_manager=mock_hda_manager, hda_id=123)
    
    # Verify
    mock_hda_manager.by_id.assert_called_once_with(123)
    mock_hda_manager._purge.assert_called_once_with(mock_hda)
```

---

## Integration Testing with Container

### Testing with Real DI Container

```python
def test_with_real_container():
    """Integration test with actual DI container."""
    from galaxy.di import Container
    
    # Create container with test configuration
    container = Container()
    container[GalaxyModelMapping] = test_model
    container[IdEncodingHelper] = test_security
    # ... configure other dependencies
    
    # Get instance from container
    manager = container[DatasetCollectionManager]
    
    # Test with real dependencies
    result = manager.some_method()
    assert result is not None
```

---

## Best Practices

### 1. Mock at the Interface Level

Mock the interface types, not concrete implementations:

```python
# Good: Mock the interface
mock_manager: HDAManager = Mock(spec=HDAManager)

# Avoid: Mocking concrete classes when interface exists
mock_manager = Mock(spec=HDAManagerImpl)  # Less flexible
```

---

### 2. Use Type Hints in Tests

Leverage type hints for better IDE support:

```python
def test_manager(mock_hda_manager: HDAManager):
    """Type hints help IDE and type checkers."""
    manager = DatasetCollectionManager(
        model=Mock(),
        security=Mock(),
        hda_manager=mock_hda_manager,
        # ... other dependencies
    )
```

---

### 3. Verify Type Contracts

Ensure mocks match expected interfaces:

```python
from unittest.mock import Mock

def test_with_typed_mock():
    """Use spec to ensure mock matches interface."""
    mock_manager = Mock(spec=HDAManager)
    # This will fail if we call methods not in HDAManager interface
    manager = DatasetCollectionManager(
        hda_manager=mock_manager,
        # ... other dependencies
    )
```

---

### 4. Test Error Cases

Test how components handle missing or invalid dependencies:

```python
def test_handles_missing_dependency():
    """Test error handling."""
    with pytest.raises(TypeError):
        # Missing required dependency
        manager = DatasetCollectionManager(
            model=Mock(),
            security=Mock(),
            # Missing hda_manager
        )
```

---

## Common Testing Patterns

### Pattern: Testing Manager with Multiple Dependencies

```python
@pytest.fixture
def manager_with_mocks():
    """Fixture providing manager with all mocked dependencies."""
    return DatasetCollectionManager(
        model=Mock(),
        security=Mock(),
        hda_manager=Mock(),
        history_manager=Mock(),
        tag_handler=Mock(),
        ldda_manager=Mock(),
    )

def test_manager_operation(manager_with_mocks):
    """Test using fixture."""
    result = manager_with_mocks.some_operation()
    assert result is not None
```

---

## Key Advantages for Testing

1. **Clear Dependencies**: Type signatures show exactly what's needed
2. **Easy Mocking**: Each dependency can be mocked independently
3. **No App Construction**: Don't need to build entire app object
4. **Type Safety**: Type hints catch errors at test time
5. **Uniform Pattern**: Same testing approach for controllers, managers, and tasks
