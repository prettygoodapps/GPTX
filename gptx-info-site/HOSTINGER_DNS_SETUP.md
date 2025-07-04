# Hostinger DNS Setup Guide for gptexchange.info

## Railway Domain Configuration Complete ✅
Railway has successfully configured your custom domain:
- **Custom Domain**: https://gptexchange.info
- **Railway Domain**: https://gptx-poc-production.up.railway.app
- **CNAME Target**: 5nhvhnj7.up.railway.app

## Step-by-Step Hostinger DNS Configuration

### 1. Access Hostinger DNS Management
1. Log into your Hostinger account at https://hpanel.hostinger.com
2. Go to **Domains** section
3. Find `gptexchange.info` and click **Manage**
4. Navigate to **DNS Zone** or **DNS Records**

### 2. Configure DNS Records

#### Option A: CNAME Record (Preferred)
```
Type:     CNAME
Name:     @ (or leave blank for root domain)
Value:    5nhvhnj7.up.railway.app
TTL:      3600 (or Auto/Default)
```

#### Option B: If CNAME @ is not supported
If Hostinger doesn't allow CNAME for root domain, use:
```
Type:     CNAME
Name:     www
Value:    5nhvhnj7.up.railway.app
TTL:      3600
```
Then add a redirect from root to www subdomain.

### 3. Remove Conflicting Records
- **Delete any existing A records** for @ or root domain
- **Remove any conflicting CNAME records**
- **Keep MX records** for email (if you use email with this domain)

### 4. Save and Wait for Propagation
- Click **Save** or **Add Record**
- DNS propagation typically takes 15-30 minutes
- Can take up to 72 hours in rare cases

## Verification Steps

### Check DNS Propagation
Use these tools to verify DNS changes:
- https://dnschecker.org
- https://whatsmydns.net
- Command line: `nslookup gptexchange.info`

### Expected Results
Once propagated, you should see:
```
gptexchange.info CNAME 5nhvhnj7.up.railway.app
```

### Test the Domain
1. Visit https://gptexchange.info
2. Should redirect to your GPTX Exchange application
3. SSL certificate will be automatically provisioned by Railway

## Troubleshooting

### If CNAME @ doesn't work:
1. Try using `www` subdomain instead
2. Set up domain forwarding in Hostinger from root to www
3. Contact Hostinger support for CNAME @ support

### If DNS doesn't propagate:
1. Clear your browser cache
2. Try incognito/private browsing
3. Use different DNS servers (8.8.8.8, 1.1.1.1)
4. Wait longer (up to 72 hours)

### Common Hostinger DNS Settings:
- **Name**: Use `@` for root domain or leave blank
- **TTL**: Use 3600 or Auto
- **Priority**: Not needed for CNAME records

## Final Result
Once configured, visitors to https://gptexchange.info will see your GPTX Exchange application with:
- ✅ Custom domain (gptexchange.info)
- ✅ SSL certificate (HTTPS)
- ✅ Prototype warning banner
- ✅ Full API functionality
- ✅ Professional appearance

## Support
If you encounter issues:
1. Check Hostinger documentation for DNS management
2. Contact Hostinger support for DNS-specific questions
3. Railway automatically handles SSL and routing once DNS is configured