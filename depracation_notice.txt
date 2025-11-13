# Deprecation Notice: [Feature/API Name]

## ⚠️ Summary
**[Feature/API Name]** is now deprecated and will be removed in **[Version X.X.X]** on **[Date]**.

## Timeline
- **Deprecation Date**: [Date] - Feature marked as deprecated
- **End of Support**: [Date] - No more bug fixes or updates
- **Removal Date**: [Date] - Feature will be completely removed

## Reason for Deprecation
[Explain why this feature is being deprecated. Examples:]
- Security vulnerabilities that cannot be patched
- Better alternatives now available
- Low usage and high maintenance cost
- Architectural improvements in newer version

## Migration Guide

### What You Need to Do
1. **Identify Usage**: Search your codebase for `[deprecated-feature]`
2. **Update Code**: Replace with the new recommended approach
3. **Test Thoroughly**: Verify functionality after migration
4. **Update Dependencies**: Ensure compatibility with new version

### Before (Deprecated)
```javascript
// Old way - DEPRECATED
const result = oldFunction(params);
```

### After (Recommended)
```javascript
// New way - RECOMMENDED
const result = newFunction(params);
```

## Alternatives

| Deprecated Feature | Recommended Alternative | Migration Difficulty |
|-------------------|------------------------|---------------------|
| `oldFunction()` | `newFunction()` | Easy |
| `OldClass` | `NewClass` | Medium |
| `legacy-endpoint` | `v2/endpoint` | Hard |

## Breaking Changes
- [List any breaking changes that come with the migration]
- [Include parameter changes, return type differences, etc.]

## Need Help?
- 📚 **Documentation**: [Link to migration guide]
- 💬 **Community Forum**: [Link to discussion]
- 🐛 **Report Issues**: [Link to issue tracker]
- 📧 **Contact Support**: [Email or support link]

## Code Examples

### Example 1: [Common Use Case]
**Before:**
```javascript
// Deprecated approach
const data = await api.oldMethod({
  param1: 'value',
  param2: 123
});
```

**After:**
```javascript
// New approach
const data = await api.newMethod({
  param1: 'value',
  param2: 123,
  options: { /* new options */ }
});
```

### Example 2: [Another Use Case]
**Before:**
```javascript
// Deprecated configuration
const config = {
  oldSetting: true,
  deprecatedOption: 'value'
};
```

**After:**
```javascript
// Updated configuration
const config = {
  newSetting: true,
  modernOption: 'value'
};
```

## FAQ

**Q: What happens if I don't migrate before the removal date?**  
A: Your application will break when upgrading to version X.X.X. We strongly recommend migrating as soon as possible.

**Q: Will there be automated migration tools?**  
A: [Yes/No - provide details if available]

**Q: Can I still use this feature in older versions?**  
A: Yes, versions prior to X.X.X will continue to support this feature, but we recommend upgrading.

**Q: Is there a grace period after the removal date?**  
A: No, the feature will be completely removed. Please plan your migration accordingly.

---

**Last Updated**: [Date]  
**Applies to Versions**: [Version range]