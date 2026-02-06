package com.debategpt.app.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.Send
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavController
import com.debategpt.app.ui.viewmodel.ChatMessage
import com.debategpt.app.ui.viewmodel.ChatbotViewModel
import com.debategpt.app.ui.viewmodel.AnalysisViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ChatbotScreen(
    navController: NavController,
    chatbotViewModel: ChatbotViewModel = viewModel(),
    analysisViewModel: AnalysisViewModel = viewModel()
) {
    val state by chatbotViewModel.uiState.collectAsState()
    val analysisState by analysisViewModel.analysisState.collectAsState()
    val winnerState by analysisViewModel.winnerState.collectAsState()
    val listState = rememberLazyListState()

    LaunchedEffect(state.messages.size) {
        if (state.messages.isNotEmpty()) {
            listState.animateScrollToItem(state.messages.size - 1)
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Chatbot Debate") },
                navigationIcon = {
                    IconButton(onClick = { navController.popBackStack() }) {
                        Icon(Icons.Filled.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
        ) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 8.dp)
            ) {
                OutlinedTextField(
                    value = state.topic,
                    onValueChange = { chatbotViewModel.setTopic(it) },
                    label = { Text("Debate Topic") },
                    placeholder = { Text("e.g. Should AI replace teachers?") },
                    modifier = Modifier.fillMaxWidth()
                )
                Spacer(modifier = Modifier.height(8.dp))
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    FilterChip(
                        selected = state.stance == "favor",
                        onClick = { chatbotViewModel.setStance("favor") },
                        label = { Text("Favor") }
                    )
                    FilterChip(
                        selected = state.stance == "against",
                        onClick = { chatbotViewModel.setStance("against") },
                        label = { Text("Against") }
                    )
                }

                // Show topic & stance summary so user sees debate setup before messages
                if (state.topic.isNotBlank()) {
                    Spacer(modifier = Modifier.height(8.dp))
                    Card(
                        modifier = Modifier.fillMaxWidth(),
                        shape = RoundedCornerShape(16.dp),
                        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
                    ) {
                        Column(modifier = Modifier.padding(12.dp)) {
                            Text(
                                text = "Debate setup",
                                style = MaterialTheme.typography.labelLarge,
                                color = MaterialTheme.colorScheme.primary
                            )
                            Spacer(modifier = Modifier.height(4.dp))
                            Text(
                                text = "Topic: ${state.topic}",
                                style = MaterialTheme.typography.bodyMedium
                            )
                            val stanceLabel = when (state.stance) {
                                "favor" -> "Favor"
                                "against" -> "Against"
                                else -> "Not selected"
                            }
                            Text(
                                text = "Your stance: $stanceLabel",
                                style = MaterialTheme.typography.bodySmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
                    }
                }
            }

            LazyColumn(
                state = listState,
                modifier = Modifier
                    .weight(1f)
                    .fillMaxWidth(),
                contentPadding = PaddingValues(16.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                items(state.messages) { msg ->
                    MessageBubble(msg)
                }
            }

            state.error?.let { error ->
                Text(
                    text = error,
                    color = MaterialTheme.colorScheme.error,
                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 4.dp)
                )
            }

            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                OutlinedTextField(
                    value = state.messageInput,
                    onValueChange = { chatbotViewModel.setMessageInput(it) },
                    placeholder = { Text("Your argument...") },
                    modifier = Modifier.weight(1f),
                    enabled = !state.isLoading
                )
                Spacer(modifier = Modifier.width(8.dp))
                FilledIconButton(
                    onClick = { chatbotViewModel.sendMessage() },
                    enabled = state.messageInput.isNotBlank() && !state.isLoading
                ) {
                    if (state.isLoading) {
                        CircularProgressIndicator(
                            modifier = Modifier.size(24.dp),
                            color = MaterialTheme.colorScheme.onPrimary
                        )
                    } else {
                        Icon(Icons.Default.Send, contentDescription = "Send")
                    }
                }
            }

            // Analysis & winner (same rich UI as STT, reusing shared composable)
            AnalysisTabContent(
                canAnalyze = state.messages.size >= 2,
                analysisState = analysisState,
                winnerState = winnerState,
                onRunAnalysis = { analysisViewModel.analyzeChatbot() },
                onGetWinner = { analysisViewModel.getWinnerChatbot() }
            )
        }
    }
}

@Composable
private fun MessageBubble(msg: ChatMessage) {
    val isUser = msg.isUser
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = if (isUser) Arrangement.End else Arrangement.Start
    ) {
        Surface(
            shape = RoundedCornerShape(
                topStart = 16.dp,
                topEnd = 16.dp,
                bottomStart = if (isUser) 16.dp else 4.dp,
                bottomEnd = if (isUser) 4.dp else 16.dp
            ),
            color = if (isUser) MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.surfaceVariant
        ) {
            Text(
                text = msg.text,
                modifier = Modifier.padding(16.dp),
                style = MaterialTheme.typography.bodyLarge
            )
        }
    }
}
