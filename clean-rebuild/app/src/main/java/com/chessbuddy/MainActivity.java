package com.chessbuddy;

import android.app.Activity;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.webkit.JavascriptInterface;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;

public final class MainActivity extends Activity {
    private WebView webView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getWindow().setStatusBarColor(Color.rgb(20, 24, 28));
        getWindow().setNavigationBarColor(Color.rgb(20, 24, 28));
        getWindow().getDecorView().setSystemUiVisibility(0);

        webView = new WebView(this);
        webView.setBackgroundColor(Color.rgb(20, 24, 28));
        webView.setOverScrollMode(WebView.OVER_SCROLL_NEVER);

        webView.getSettings().setJavaScriptEnabled(true);
        webView.getSettings().setDomStorageEnabled(true);
        webView.getSettings().setAllowFileAccess(true);
        webView.getSettings().setAllowContentAccess(false);
        webView.getSettings().setAllowFileAccessFromFileURLs(false);
        webView.getSettings().setAllowUniversalAccessFromFileURLs(false);
        webView.getSettings().setSupportZoom(false);
        webView.getSettings().setBuiltInZoomControls(false);

        webView.addJavascriptInterface(new AndroidBridge(), "AndroidBridge");
        webView.setWebChromeClient(new WebChromeClient());
        webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                return !("file".equals(request.getUrl().getScheme())
                        && "/android_asset/index.html".equals(request.getUrl().getPath()));
            }
        });

        setContentView(webView);
        webView.loadUrl("file:///android_asset/index.html");
    }

    @Override
    @SuppressWarnings("deprecation")
    public void onBackPressed() {
        if (webView != null && webView.canGoBack()) {
            webView.goBack();
        } else {
            super.onBackPressed();
        }
    }

    @Override
    protected void onDestroy() {
        if (webView != null) {
            webView.removeJavascriptInterface("AndroidBridge");
            webView.destroy();
            webView = null;
        }
        super.onDestroy();
    }

    public final class AndroidBridge {
        @JavascriptInterface
        public void shareText(String text) {
            if (text == null || text.length() > 200000) return;
            runOnUiThread(() -> {
                Intent send = new Intent(Intent.ACTION_SEND);
                send.setType("text/plain");
                send.putExtra(Intent.EXTRA_TEXT, text);
                startActivity(Intent.createChooser(send, "Share chess game"));
            });
        }

        @JavascriptInterface
        public void copyText(String text) {
            if (text == null || text.length() > 200000) return;
            runOnUiThread(() -> {
                ClipboardManager clipboard =
                        (ClipboardManager) getSystemService(Context.CLIPBOARD_SERVICE);
                if (clipboard != null) {
                    clipboard.setPrimaryClip(ClipData.newPlainText("ChessBuddy", text));
                    Toast.makeText(MainActivity.this, "Copied", Toast.LENGTH_SHORT).show();
                }
            });
        }
    }
}
