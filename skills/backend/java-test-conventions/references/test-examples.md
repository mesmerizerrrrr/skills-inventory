# 분기별 테스트와 fixture 예시

다음 예시의 기존 구현 계약은 `MessageService.sendMessage(MessageRequest)`다. 정상 요청이면 `MessageGateway.send(request)`에 위임하고, 수신자가 비어 있으면 `IllegalArgumentException`을 발생시키며 발송하지 않는다. `MessageRequest`는 `(recipient, content)` 생성자를 제공한다고 가정한다. 실제 프로젝트의 타입·생성 API·예외 계약에 맞춰 적용하며, 예시에 맞추려고 구현을 수정하지 않는다.

## 기능별 fixture

`src/test/java/.../message/fixture/MessageFixture.java`에 둔다. 정상 요청과 수신자 누락 요청이 여러 테스트에서 재사용되는 상황의 예시다.

```java
public final class MessageFixture {

    private MessageFixture() {
    }

    public static MessageRequest validMessage() {
        return new MessageRequest("recipient-001", "안내 메시지");
    }

    public static MessageRequest messageWithoutRecipient() {
        return new MessageRequest("", "안내 메시지");
    }

}
```

fixture는 호출마다 새 객체를 만든다. 다른 도메인의 fixture는 해당 도메인에 따로 두며, 한 테스트에서만 필요한 간단한 값까지 공통 라이브러리로 확장하지 않는다.

## 정상·예외 분기를 각각 검증

아래는 JUnit Jupiter, Mockito, AssertJ를 사용하는 예시다. 프로젝트에 이미 다른 assertion 도구가 있으면 같은 검증 구조로 맞춘다. `MessageServiceTest`는 `src/test/java`의 실제 구현과 대응되는 패키지에 둔다.

```java
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.catchThrowable;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.verifyNoInteractions;

class MessageServiceTest {

    private MessageGateway messageGateway;
    private MessageService messageService;

    @BeforeEach
    void setUp() {
        messageGateway = mock(MessageGateway.class);
        messageService = new MessageService(messageGateway);
    }

    @Test
    @DisplayName("정상 메시지는 발송 처리한다")
    void sendMessage() {

        // given
        MessageRequest request = MessageFixture.validMessage();

        // when
        messageService.sendMessage(request);

        // then
        verify(messageGateway).send(request);
    }

    @Test
    @DisplayName("수신자가 없으면 예외가 발생하고 메시지를 발송하지 않는다")
    void sendMessage_whenRecipientMissing() {

        // given
        MessageRequest request = MessageFixture.messageWithoutRecipient();

        // when
        Throwable thrown = catchThrowable(() -> messageService.sendMessage(request));

        // then
        assertThat(thrown).isInstanceOf(IllegalArgumentException.class);
        verifyNoInteractions(messageGateway);
    }

}
```

업무 오류 코드·메시지가 계약에 포함되어 있으면 `then`에서 함께 검증한다. 성공 테스트 하나에서 정상 요청을 발송한 뒤 잘못된 요청까지 다시 실행하지 않는다. `catchThrowable` 대신 JUnit의 `assertThrows`를 사용한다면 대상 실행과 예외 포착을 `when`에 두고, `then`에서 예외의 의미 있는 속성·부수효과를 확인한다.
